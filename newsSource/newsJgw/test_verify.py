from keras_bert import Tokenizer,load_trained_model_from_checkpoint
from keras.models import load_model
import json
import codecs
import numpy as np
mode = 0
maxlen = 160
learning_rate = 5e-5
min_learning_rate = 1e-5

config_path = './chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = './chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = './chinese_L-12_H-768_A-12/vocab.txt'

#Make Tonkenizer
token_dict = {}

with codecs.open(dict_path, 'r', 'utf8') as reader:
    for line in reader:
        token = line.strip()
        token_dict[token] = len(token_dict)


class OurTokenizer(Tokenizer):
    def _tokenize(self, text):
        R = []
        for c in text:
            if c in self._token_dict:
                R.append(c)
            elif self._is_space(c):
                R.append('[unused1]') # space类用未经训练的[unused1]表示
            else:
                R.append('[UNK]') # 剩余的字符是[UNK]
        return R

tokenizer = OurTokenizer(token_dict)

tokenizer = OurTokenizer(token_dict)

from keras.layers import *
from keras.models import Model
import keras.backend as K
from keras.callbacks import Callback
from keras.optimizers import Adam

#load classes
id2predicate, predicate2id = json.load(open('./datasets/all_50_schemas_me.json',encoding='utf-8'))
id2predicate = {int(i):j for i,j in list(id2predicate.items())}
num_classes = len(id2predicate)

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


bert_model = load_trained_model_from_checkpoint(config_path, checkpoint_path, seq_len=None)

for l in bert_model.layers:
    l.trainable = True

t1_in = Input(shape=(None,))
t2_in = Input(shape=(None,))
s1_in = Input(shape=(None,))
s2_in = Input(shape=(None,))
k1_in = Input(shape=(1,))
k2_in = Input(shape=(1,))
o1_in = Input(shape=(None, num_classes))
o2_in = Input(shape=(None, num_classes))

t1, t2, s1, s2, k1, k2, o1, o2 = t1_in, t2_in, s1_in, s2_in, k1_in, k2_in, o1_in, o2_in
mask = Lambda(lambda x: K.cast(K.greater(K.expand_dims(x, 2), 0), 'float32'))(t1)#建一个以t1为输入层，将t1添加一个维度后数值先转为bool再转为float
t = bert_model([t1, t2])
ps1 = Dense(1, activation='sigmoid')(t)
ps2 = Dense(1, activation='sigmoid')(t)

subject_model = Model([t1_in, t2_in], [ps1, ps2]) # 预测subject的模型

k1v = Lambda(seq_gather)([t, k1])
k2v = Lambda(seq_gather)([t, k2])
kv = Average()([k1v, k2v])
t = Add()([t, kv])
po1 = Dense(num_classes, activation='sigmoid')(t)
po2 = Dense(num_classes, activation='sigmoid')(t)

object_model = Model([t1_in, t2_in, k1_in, k2_in], [po1, po2]) # 输入text和subject，预测object及其关系

train_model = Model([t1_in, t2_in, s1_in, s2_in, k1_in, k2_in, o1_in, o2_in],
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

train_model.add_loss(loss)
train_model.compile(optimizer=Adam(learning_rate))
train_model.summary()
train_model.load_weights('best_model.weights')

def extract_items(text_in):
    _tokens = tokenizer.tokenize(text_in)
    _t1, _t2 = tokenizer.encode(first=text_in)
    _t1, _t2 = np.array([_t1]), np.array([_t2])
    _k1, _k2 = subject_model.predict([_t1, _t2])
    _k1, _k2 = np.where(_k1[0] > 0.5)[0], np.where(_k2[0] > 0.4)[0]
    _subjects = []
    for i in _k1:
        j = _k2[_k2 >= i]
        if len(j) > 0:
            j = j[0]
            _subject = text_in[i-1: j]
            _subjects.append((_subject, i, j))
    if _subjects:
        R = []
        _t1 = np.repeat(_t1, len(_subjects), 0)
        _t2 = np.repeat(_t2, len(_subjects), 0)
        _k1, _k2 = np.array([_s[1:] for _s in _subjects]).T.reshape((2, -1, 1))
        _o1, _o2 = object_model.predict([_t1, _t2, _k1, _k2])
        for i,_subject in enumerate(_subjects):
            _oo1, _oo2 = np.where(_o1[i] > 0.5), np.where(_o2[i] > 0.4)
            for _ooo1, _c1 in zip(*_oo1):
                for _ooo2, _c2 in zip(*_oo2):
                    if _ooo1 <= _ooo2 and _c1 == _c2:
                        _object = text_in[_ooo1-1: _ooo2]
                        _predicate = id2predicate[_c1]
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

# tempEx=extract_items("《流浪地球》是由中国电影股份有限公司、北京京西文化旅游股份有限公司、北京登峰国际文化传播有限公司、郭帆文化传媒（北京）有限公司出品的科幻片，由郭帆执导，吴京特别出演，屈楚萧、李光洁、吴孟达、赵今麦领衔主演。该片于2019年2月5日（农历大年初一）在中国内地上映。")
# tempEx=extract_items("国民信托产品违约僵局待解 董事长建议投资者起诉公司海航质疑*ST九龙(600555)案判决 李勤夫方董事会或重新控制公司")
pass