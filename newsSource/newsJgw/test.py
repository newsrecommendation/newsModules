import json
Data=[]
temp=json.load(open("pathConfig.json","r"))
with open("./NewYorkTimes/train.json") as f:
    for line in f:
        Data.append(eval(line))
RelationSet=list()
for x in [x['relationMentions'] for x in Data]:
    for x1 in x:
        RelationSet.append(x1['label'])
RelationSet=set(RelationSet)
print()

