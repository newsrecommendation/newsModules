from peewee import *
import random
from tqdm import trange
import pandas as pd
db = MySQLDatabase("test", host="localhost", port=3306, user="root", passwd="123")
db.connect()
class news_collection(Model):
    news_id=PrimaryKeyField()
    news_title=TextField()
    news_entity=TextField()
    news_entity_permID=TextField()
    news_content=TextField()
    class Meta:
        database=db
class permID_relation(Model):
    relation_id=PrimaryKeyField()
    subject=TextField()
    relation=IntegerField()
    object=TextField()
    class Meta:
        database=db
news_collection.bind(db)
permID_relation.bind(db)
allPermId=set()
selector = news_collection.select().where(news_collection.news_entity_permID != "None")
for x in selector:
    allPermId.add(x.news_entity_permID)
permIndex=list(allPermId)
allPermId=list(allPermId)

relations=[]
for x in permIndex:
    random.shuffle(allPermId)
    for i in range(50):
        # relations.append([x,random.randint(0,5),allPermId[i]])
        relations.append({
            "subject":x,
            "relation":random.randint(0,5),
            "object":allPermId[i]
        })
# with db.atomic():
#     for i in trange(0, len(relations), 100):
#         # news_collection.create(**tempInsert)
#         permID_relation.insert_many(relations[i:i + 100]).execute()
relations=[]
selector=permID_relation.select()
for x in selector:
    # print()
    relations.append([int(x.subject),x.relation,int(x.object)])

pd.DataFrame(relations).to_csv("jgw_classtriples.txt",header=False,index=False,sep='\t')
print()
