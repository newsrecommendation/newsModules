import pandas as pd
from newsExtracter import Extracter
from tqdm import trange


import numpy as np


with open("./ccks2019/result.txt","r") as f:
    with open("./ccks2019/resultFinal.txt","w") as f1:
        i=3000000
        for temp in f:
            f1.write(str(i)+","+temp)
            i+=1

f.close()
f1.close()
pd.DataFrame(Data)[0].to_csv("./ccks2019/result.txt",header=None)

# import tqdm
Data=pd.read_csv("./ccks2019/event_type_entity_extract_test.csv",header=None)
Data=Data[1]
# Data=[]
# with open('./ccks2019/event_type_entity_extract_test.csv') as f:
#     while True
#     Data.append(f.readline())
extracter=Extracter()
extracter.createSubjectModel()
# extracter.createNTripleModel()
# print(extracter.extractSubject("暴风集团董事长冯鑫因涉嫌犯罪被公安机关采取强制措施，有市场人士指出或因其在收购MPS的融资过程中有违法行为"))
# print(extracter.extractNTriple("龙政，男，汉族，1954年10月出生，湖北省浠水县人，1978年8月参加工作，1974年1月加入中国共产党，大学本科学历，硕士学位，研究员"))
# print(extracter.getRelation())

with open("./ccks2019/result.txt","w") as f:
    for i in trange(len(Data)):
    # for x in Data:
        result=extracter.extractSubject(Data[i])
        if len(result)!=0:
            f.write(result[0][0])
        f.write('\n')

f.close()
print()

