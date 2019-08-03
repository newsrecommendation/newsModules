from keras_bert import Tokenizer,load_trained_model_from_checkpoint
import codecs
# import numpy as np
import json


from keras.layers import *
import keras.backend as K
from keras.models import Model
from keras.optimizers import Adam
import tensorflow as tf

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
def seq_gather(x):
    """seq是[None, seq_len, s_size]的格式，
    idxs是[None, 1]的格式，在seq的第i个序列中选出第idxs[i]个向量，
    最终输出[None, s_size]的向量。
    """
    seq, idxs = x
    idxs = K.cast(idxs, 'int32')          #把idxs转成int32的dtype
    batch_idxs = K.arange(0, K.shape(seq)[0])  #列出一个[0,1,2...len（seq）-1]的序列
    batch_idxs = K.expand_dims(batch_idxs, 1)#给这个序列增加一维
    idxs = K.concatenate([batch_idxs, idxs], 1)#把这个序列和index连接起来
    return K.tf.gather_nd(seq, idxs)#但最后只是选出了idxs所指定的第i个向量？
class Extracter:
    def __init__(self):
        self.path = json.load(open('pathConfig.json', 'r'))
        self.SubjectTrainModel=Model()
        self.SubjectPredModel=Model()
        self.NTripleTrainModel=Model()
        self.NTripleSubjectModel=Model()
        self.NTripleObjectModel=Model()
        # self.bertModel = load_trained_model_from_checkpoint(self.path["bertConfig"], self.path["bertCheckPoint"], seq_len=None)
        self.SubjectBertModel=None
        self.NTripleBertModel=None
        self.classBertModel=None
        self.tokenizer = getTokneizer(self.path['vocabDict'])
    def createSubjectModel(self):
        if not self.SubjectBertModel:
            self.SubjectBertModel = load_trained_model_from_checkpoint(self.path["bertConfig"], self.path["bertCheckPoint"], seq_len=None)
        TextEncode = Input(shape=(None,))
        TextSegment = Input(shape=(None,))
        SubjectStart = Input(shape=(None,))
        SubjectEnd = Input(shape=(None,))
        Mask = Lambda(lambda x: K.cast(K.greater(K.expand_dims(x, -1), 0), 'float32'))(TextEncode)
        bertLayer = self.SubjectBertModel([TextEncode, TextSegment])
        SubPredStart = Dense(1, use_bias=False)(bertLayer)
        SubPredStart = Lambda(lambda x: x[0][..., 0] - (1 - x[1][..., 0]) * 1e10)([SubPredStart, Mask])
        SubPredEnd = Dense(1, use_bias=False)(bertLayer)
        SubPredEnd = Lambda(lambda x: x[0][..., 0] - (1 - x[1][..., 0]) * 1e10)([SubPredEnd, Mask])

        self.SubjectPredModel = Model([TextEncode, TextSegment], [SubPredStart, SubPredEnd])
        self.SubjectTrainModel = Model([TextEncode, TextSegment, SubjectStart, SubjectEnd], [SubPredStart, SubPredEnd])

        loss1 = K.mean(K.categorical_crossentropy(SubjectStart, SubPredStart, from_logits=True))
        SubPredEnd -= (1 - K.cumsum(SubjectStart, 1)) * 1e10
        loss2 = K.mean(K.categorical_crossentropy(SubjectEnd, SubPredEnd, from_logits=True))
        FinalLoss = loss1 + loss2

        self.SubjectTrainModel.add_loss(FinalLoss)
        # self.SubjectTrainModel.compile(optimizer=Adam(lr=0.001))
        # self.SubjectTrainModel.summary()
        self.SubjectTrainModel.load_weights('./data/SubjectWeights')
    def extractSubject(self,text_in):
        _tokens = self.tokenizer.tokenize(text_in)
        _t1, _t2 = self.tokenizer.encode(first=text_in)
        _t1, _t2 = np.array([_t1]), np.array([_t2])
        _k1, _k2 = self.SubjectPredModel.predict([_t1, _t2])
        # _k1, _k2 = np.where(_k1[0] > 0.5)[0], np.where(_k2[0] > 0.4)[0]
        _k1,_k2=np.where(_k1[0]==max(_k1[0]))[0],np.where(_k2[0]==max(_k2[0]))[0]
        _subjects = []
        for i in _k1:
            j = _k2[_k2 >= i]
            if len(j) > 0:
                j = j[0]
                _subject = text_in[i-1: j-1]
                _subjects.append((_subject, i, j))
            return list(_subjects)
    def createNTripleModel(self):
        if not self.NTripleBertModel:
            self.NTripleBertModel = load_trained_model_from_checkpoint(self.path["bertConfig"], self.path["bertCheckPoint"], seq_len=None)

        self.id2predicate, predicate2id = json.load(open(self.path['Relation'], encoding='utf-8'))
        self.id2predicate = {int(i): j for i, j in list(self.id2predicate.items())}
        num_classes = len(self.id2predicate)

        t1_in = Input(shape=(None,))
        t2_in = Input(shape=(None,))
        s1_in = Input(shape=(None,))
        s2_in = Input(shape=(None,))
        k1_in = Input(shape=(1,))
        k2_in = Input(shape=(1,))
        o1_in = Input(shape=(None, num_classes))
        o2_in = Input(shape=(None, num_classes))
        t1, t2, s1, s2, k1, k2, o1, o2 = t1_in, t2_in, s1_in, s2_in, k1_in, k2_in, o1_in, o2_in
        mask = Lambda(lambda x: K.cast(K.greater(K.expand_dims(x, 2), 0), 'float32'))(t1)  # 建一个以t1为输入层，将t1添加一个维度后数值先转为bool再转为float
        t = self.NTripleBertModel([t1, t2])
        ps1 = Dense(1, activation='sigmoid')(t)
        ps2 = Dense(1, activation='sigmoid')(t)

        self.NTripleSubjectModel = Model([t1_in, t2_in], [ps1, ps2])  # 预测subject的模型

        k1v = Lambda(seq_gather)([t, k1])
        k2v = Lambda(seq_gather)([t, k2])
        kv = Average()([k1v, k2v])
        t = Add()([t, kv])
        po1 = Dense(num_classes, activation='sigmoid')(t)
        po2 = Dense(num_classes, activation='sigmoid')(t)

        self.NTripleObjectModel = Model([t1_in, t2_in, k1_in, k2_in], [po1, po2])  # 输入text和subject，预测object及其关系

        self.NTripleTrainModel = Model([t1_in, t2_in, s1_in, s2_in, k1_in, k2_in, o1_in, o2_in],
                            [ps1, ps2, po1, po2])

        s1 = K.expand_dims(s1, 2)
        s2 = K.expand_dims(s2, 2)

        s1_loss = K.binary_crossentropy(s1, ps1)
        s1_loss = K.sum(s1_loss * mask) / K.sum(mask)
        s2_loss = K.binary_crossentropy(s2, ps2)
        s2_loss = K.sum(s2_loss * mask) / K.sum(mask)

        o1_loss = K.sum(K.binary_crossentropy(o1, po1), 2, keepdims=True)
        o1_loss = K.sum(o1_loss * mask) / K.sum(mask)
        o2_loss = K.sum(K.binary_crossentropy(o2, po2), 2, keepdims=True)
        o2_loss = K.sum(o2_loss * mask) / K.sum(mask)

        loss = (s1_loss + s2_loss) + (o1_loss + o2_loss)

        self.NTripleTrainModel.add_loss(loss)
        # self.NTripleTrainModel.compile(optimizer=Adam(learning_rate))
        # self.NTripleTrainModel.summary()
        self.NTripleTrainModel.load_weights('./data/NTripleWeights')
    def extractNTriple(self,text_in):
        _tokens = self.tokenizer.tokenize(text_in)
        _t1, _t2 = self.tokenizer.encode(first=text_in)
        _t1, _t2 = np.array([_t1]), np.array([_t2])
        _k1, _k2 = self.NTripleSubjectModel.predict([_t1, _t2])
        _k1, _k2 = np.where(_k1[0] > 0.5)[0], np.where(_k2[0] > 0.4)[0]
        _subjects = []
        for i in _k1:
            j = _k2[_k2 >= i]
            if len(j) > 0:
                j = j[0]
                _subject = text_in[i - 1: j]
                _subjects.append((_subject, i, j))
        if _subjects:
            R = []
            _t1 = np.repeat(_t1, len(_subjects), 0)
            _t2 = np.repeat(_t2, len(_subjects), 0)
            _k1, _k2 = np.array([_s[1:] for _s in _subjects]).T.reshape((2, -1, 1))
            _o1, _o2 = self.NTripleObjectModel.predict([_t1, _t2, _k1, _k2])
            for i, _subject in enumerate(_subjects):
                _oo1, _oo2 = np.where(_o1[i] > 0.5), np.where(_o2[i] > 0.4)
                for _ooo1, _c1 in zip(*_oo1):
                    for _ooo2, _c2 in zip(*_oo2):
                        if _ooo1 <= _ooo2 and _c1 == _c2:
                            _object = text_in[_ooo1 - 1: _ooo2]
                            _predicate = self.id2predicate[_c1]
                            R.append((_subject[0], _predicate, _object))
                            break
            zhuanji, gequ = [], []
            for s, p, o in R[:]:
                if p == '妻子':
                    R.append((o, '丈夫', s))
                elif p == '丈夫':
                    R.append((o, '妻子', s))
                if p == '所属专辑':
                    zhuanji.append(o)
                    gequ.append(s)
            spo_list = set()
            for s, p, o in R:
                if p in ['歌手', '作词', '作曲']:
                    if s in zhuanji and s not in gequ:
                        continue
                spo_list.add((s, p, o))
            return list(spo_list)
        else:
            return []
    def getRelation(self):
        relations=list(json.load(open(self.path['Relation'], encoding='utf-8'))[1])
        return relations
    def createClassModel(self):
        self.classDict = json.load(open("./data/ccks2019/classes.json"))
        if not self.classBertModel:
            self.classBertModel = load_trained_model_from_checkpoint(self.path["bertConfig"], self.path["bertCheckPoint"], seq_len=None)
        TextEncode = Input(shape=(None,))
        TextSegment = Input(shape=(None,))

        classInput = Input(shape=(None,))
        Mask = Lambda(lambda x: K.cast(K.greater(K.expand_dims(x, -1), 0), 'float32'))(TextEncode)
        bertLayer = self.classBertModel([TextEncode, TextSegment])

        classPred = Dense(len(self.classDict[1]), use_bias=False)(bertLayer)
        classPred = Lambda(lambda x: K.sum(x, axis=1))(classPred)

        self.classPredModel = Model([TextEncode, TextSegment], [classPred])
        self.classTrainModel = Model([TextEncode, TextSegment, classInput], [classPred])

        self.classTrainModel.load_weights('./data/classWeights')
    def extractClass(self,text_in):
        _tokens = self.tokenizer.tokenize(text_in)
        _t1, _t2 = self.tokenizer.encode(first=text_in)
        _t1, _t2 = np.array([_t1]), np.array([_t2])
        classPred = self.classPredModel.predict([_t1, _t2])
        # _k1, _k2 = np.where(_k1[0] > 0.5)[0], np.where(_k2[0] > 0.4)[0]
        return [self.classDict[0][str(x)] for x in list(np.where(classPred[0]==max(classPred[0]))[0])]
