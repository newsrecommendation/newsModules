from __future__ import unicode_literals
import pandas as pd
from keras_bert import Tokenizer,load_trained_model_from_checkpoint
import codecs
import numpy as np
import json
import keras
from keras.utils import to_categorical

path=json.load(open('pathConfig.json','r'))

Data=pd.read_csv(path['trainData'],header=None,error_bad_lines=False)
Data=Data[Data[2]!= u'其他']
def creadteClassDict():
    classes=list(set(Data[2]))
    finalDict=[]
    i=0
    idDict,classDict={},{}
    for x in classes:
        idDict[i]=x
        classDict[x]=i
        i+=1
    finalDict.append(idDict)
    finalDict.append(classDict)
    json.dump(finalDict,open("./ccks2019/classes.json",'w',encoding='utf-8'),ensure_ascii=False)
classDict=json.load(open("./ccks2019/classes.json"))
trainData=list(Data[1])

class ourTokenizer(Tokenizer):
    def _tokenize(self, text):
        result=[]
        for word in text:
            if word in self._token_dict:
                result.append(word)
            elif self._is_space(word):
                result.append('[unused1]')
            else:
                result.append('[UNK]')
        return result

def getTokneizer(path):
    result={}
    with codecs.open(path,'r','utf-8') as reader:
        for line in reader:
            result[line.strip()]=len(result)
    return ourTokenizer(result)

tokenizer=getTokneizer(path['vocabDict'])

def pad_list(lst):
    inner_max_len = max(map(len, lst))
    for i in range(len(lst)):
        lst[i].extend([0]*(inner_max_len-len(lst[i])))

    return np.array(lst)



class DataGenerator:
    def __init__(self,trainData,tokenizer,maxLength=200,batchSize=32):
        self.data=trainData
        self.batchSize=batchSize
        self.length=len(self.data)//batchSize
        if self.length%batchSize!=0:
            self.length+=1
        self.tokenizer=tokenizer
        self.maxLength=maxLength
    def __len__(self):
        return self.length
    def __iter__(self):
        while True:
            np.random.shuffle(self.data)
            currentStep=0
            while currentStep<=self.length:
                if currentStep==self.length:
                    currentData=self.data[(currentStep-1)*self.batchSize:]
                else:
                    currentData=self.data[currentStep*self.batchSize : (currentStep+1)*self.batchSize]
                # T1,T2=[tokenizer.encode(x[1]) for x in currentData]
                # if len(x[1])>self.maxLength:
                #     x[1]=x[1][:self.maxLength]
                T1,T2,t1,t2,S1,S2,K1=[],[],[],[],[],[],[]
                numClasses=len(classDict[1])
                for x in currentData:
                    K1.append(to_categorical(classDict[1][x[2]],num_classes=numClasses))
                    if len(x[1])>self.maxLength:
                        x[1]=x[1][:self.maxLength]
                    t1,t2=tokenizer.encode(x[1])
                    T1.append(t1)
                    T2.append(t2)
                # T1=[element[0] for element in [tokenizer.encode(x[1]) for x in currentData]]
                T1=pad_list(T1)
                # T2=np.zeros(shape=T1.shape)
                T2=pad_list(T2)
                S1,S2=[],[]
                for x in currentData:
                    start=x[1].find(x[3])+1
                    s1, s2 = np.zeros(len(T1[0])), np.zeros(len(T1[0]))
                    if start!=0 and start<len(T1[0]):
                        s1[start]=1
                        s2[start+len(x[3])]=1
                    S1.append(s1)
                    S2.append(s2)
                        # S1.append(start)
                        # S2.append(start+len(x[3]))
                S1=np.array(S1)
                S2=np.array(S2)
                K1=np.array(K1)
                currentStep+=1
                # yield [T1,T2,S1,S2,K1],None
                yield [T1,T2,K1],None

dataGenerator=DataGenerator(Data.as_matrix(),tokenizer)
tempX=iter(dataGenerator)
# while True:
#     temps=next(tempX)
# temps=next(tempX)


from keras.layers import *
import keras.backend as K
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import Callback
import tensorflow as tf
bertModel=load_trained_model_from_checkpoint(path["bertConfig"],path["bertCheckPoint"],seq_len=None)
for layer in bertModel.layers:
    layer.trainable=True

# TextEncode=Input(shape=(None,))
# TextSegment=Input(shape=(None,))
# bertLayer=bertModel([TextEncode,TextSegment])
# SubPredStart=Dense(1,activation='sigmoid')(bertLayer)
# SubPredEnd=Dense(1,activation='sigmoid')(bertLayer)
# SubjectStart=Input(shape=(None,))
# SubjectEnd=Input(shape=(None,))
#
# SubjectStartEx=K.expand_dims(SubjectStart,-1)
# SubjectEndEx=K.expand_dims(SubjectEnd,-1)
#
# SubStartLoss=K.binary_crossentropy(SubjectStartEx,SubPredStart)
# SubEndLoss=K.binary_crossentropy(SubjectEndEx,SubPredEnd)
# Mask=Lambda(lambda x:K.cast(K.greater(K.expand_dims(x,-1),0),'float32'))(TextEncode)
# SubStartLoss=K.sum(SubStartLoss*Mask)/K.sum(Mask)
# SubEndLoss=K.sum(SubEndLoss*Mask)/K.sum(Mask)
# FinalLoss=SubStartLoss+SubEndLoss

TextEncode=Input(shape=(None,))
TextSegment=Input(shape=(None,))
# SubjectStart=Input(shape=(None,))
# SubjectEnd=Input(shape=(None,))
classInput=Input(shape=(None,))
Mask=Lambda(lambda x:K.cast(K.greater(K.expand_dims(x,-1),0),'float32'))(TextEncode)
bertLayer=bertModel([TextEncode,TextSegment])
# SubPredStart=Dense(1,use_bias=False)(bertLayer)
# SubPredStart = Lambda(lambda x: x[0][..., 0] - (1 - x[1][..., 0]) * 1e10)([SubPredStart, Mask])
# SubPredEnd=Dense(1,use_bias=False)(bertLayer)
# SubPredEnd = Lambda(lambda x: x[0][..., 0] - (1 - x[1][..., 0]) * 1e10)([SubPredEnd, Mask])

# subjectModel=Model([TextEncode,TextSegment],[SubPredStart,SubPredEnd])

classPred=Dense(len(classDict[1]),use_bias=False)(bertLayer)
classPred=Lambda(lambda x:K.sum(x,axis=1))(classPred)

# classPred=Lambda(lambda x:K.sum(x,axis=1))(classPred)


classModel=Model([TextEncode,TextSegment],[classPred])
trainModel=Model([TextEncode,TextSegment,classInput],[classPred])

# loss1 = K.mean(K.categorical_crossentropy(SubjectStart, SubPredStart, from_logits=True))
# SubPredEnd -= (1 - K.cumsum(SubjectStart, 1)) * 1e10
# loss2 = K.mean(K.categorical_crossentropy(SubjectEnd, SubPredEnd, from_logits=True))
loss3=K.mean(K.categorical_crossentropy(classInput,classPred,from_logits=True))
# FinalLoss = loss1 + loss2+loss3

learning_rate=5e-5
min_learning_rate=1e-5

trainModel.add_loss(loss3)
trainModel.compile(optimizer=Adam(lr=learning_rate))
trainModel.summary()


class Evaluate(Callback):
    def __init__(self):
        self.ACC = []
        self.best = 0.
        self.passed = 0
    def on_batch_begin(self, batch, logs=None):
        """第一个epoch用来warmup，第二个epoch把学习率降到最低
        """
        if self.passed < self.params['steps']:
            lr = (self.passed + 1.) / self.params['steps'] * learning_rate
            K.set_value(self.model.optimizer.lr, lr)
            self.passed += 1
        elif self.params['steps'] <= self.passed < self.params['steps'] * 2:
            lr = (2 - (self.passed + 1.) / self.params['steps']) * (learning_rate - min_learning_rate)
            lr += min_learning_rate
            K.set_value(self.model.optimizer.lr, lr)
            self.passed += 1
    def on_epoch_end(self, epoch, logs=None):
        trainModel.save_weights('classWeights')

evalutor=Evaluate()
trainModel.fit_generator(dataGenerator.__iter__(),
                         steps_per_epoch=1500,
                         epochs=30,
                         callbacks=[evalutor])
print("Finished!")