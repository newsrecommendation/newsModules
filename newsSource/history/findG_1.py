from __future__ import unicode_literals
from Things_Define_MainNER_Triple.newsExtracter import Extracter
import json
from collections import Counter
from tqdm import trange

def find_most_entity(filename):
    Datas = []
    # Results = []
    # result={
    #     "enity":[],
    #     "event":[]
    # }
    with open(filename,'r') as f:
        Datas.append([])
        for lines in f:
            for x in lines.split('。'):
                x = x.strip()
                if len(x) > 5:
                    Datas[-1].append(x)
    extracter = Extracter()
    # extracter.createClassModel()
    extracter.createSubjectModel()
    # extracter.createNTripleModel()
    print("Input Text")
    # result=extracter.extractClass("金蝶纯利增长达34%创四年同期新高")
    # while True:
    #     print(extracter.extractClass(input()))
    result = {
        "enity": [],
        # "event": [],
        "commonEnity": [],
        # "commonEvent": []
    }
    for passage in Datas:
        for i in trange(len(passage)):
            currentEnity = extracter.extractSubject(passage[i])
            # currentEvent = extracter.extractClass(passage[i])
            if currentEnity:
                result["enity"].append(currentEnity[0][0])
                # result["event"].append(currentEvent[0])
        result["commonEnity"] = Counter(result["enity"]).most_common()
        # result["commonEvent"] = Counter(result["event"]).most_common()
        # Results.append(result)
    print(result["commonEnity"][0][0])
    return (result["commonEnity"][0][0])

# json.dump(Results,open("./RealNews/ExtractResult.json",'w'),ensure_ascii=False)
# print(result)

find_most_entity('股票/' + str(644579) + '.txt')
