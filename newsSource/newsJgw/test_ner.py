import sys
import numpy as np
from keras_bert import load_vocabulary, load_trained_model_from_checkpoint, Tokenizer, get_checkpoint_paths

print('This demo demonstrates how to load the pre-trained model and extract word embeddings')

# if len(sys.argv) == 2:
#     model_path = sys.argv[1]
# else:
#     from keras_bert.datasets import get_pretrained, PretrainedList
#     model_path = get_pretrained(PretrainedList.chinese_base)

model_path="./chinese_L-12_H-768_A-12"
paths = get_checkpoint_paths(model_path)

model = load_trained_model_from_checkpoint(paths.config, paths.checkpoint, seq_len=10)
model.summary(line_length=120)

token_dict = load_vocabulary(paths.vocab)

tokenizer = Tokenizer(token_dict)
# text = '近年来，我国金融控股公司发展较快，有利于满足各类企业和消费者对多元化金融服务的需求，提升服务经济高质量发展的能力。但实践中有一些金融控股公司，主要是非金融企业投资形成的金融控股公司盲目向金融业扩张，将金融机构作为“提款机”，存在监管真空，风险不断累积和暴露。为有序整顿和约束事实上已形成的金融控股集团的风险，同时有效规范增量，防范金融风险跨行业、跨市场传递，《办法》根据党中央、国务院决策部署，按照问题导向，补齐监管制度短板，遵循宏观审慎管理理念，以并表监管为基础，对金融控股公司的资本、行为及风险进行全面、持续、穿透监管。'
text='哈尔滨'
tokens = tokenizer.tokenize(text)
print('Tokens:', tokens)
indices, segments = tokenizer.encode(first=text, max_len=10)

predicts = model.predict([np.array([indices]), np.array([segments])])[0]
for i, token in enumerate(tokens):
    print(token, predicts[i].tolist()[:5])