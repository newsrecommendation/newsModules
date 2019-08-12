from peewee import *
from tqdm import trange
import os

path="./Stock/"
files=os.listdir(path)
# for root, dirs, files in os.walk(path):
#     print()
data=[]
for i in trange(len(files)):
    with open(path+"/"+files[i]) as f:
        flag=True
        title=""
        content=""
        for lines in f:
            if flag:
                title=lines.strip()
                flag=False
            else:
                content=content+"\n"
                content=content+ lines.strip()
        content=content[1:]
        tempInsert={
            "news_title":title,
            "news_content":content
        }
        data.append(tempInsert)

db = MySQLDatabase("test", host="localhost", port=3306, user="root", passwd="123")
db.connect()
class raw_news(Model):
    news_id=PrimaryKeyField()
    news_title=TextField()
    news_content=TextField()
    class Meta:
        dataBase=db
class news_collection(Model):
    news_id=PrimaryKeyField()
    news_title=TextField()
    news_entity=TextField()
    news_entity_permID=TextField()
    news_content=TextField()
    class Meta:
        database=db

# testNews=news_collection.get(news_collection.news_id==1)
testNews=news_collection.select()

#
raw_news.bind(db)
with db.atomic():
    for i in trange(0,len(data),100):
        # news_collection.create(**tempInsert)
        raw_news.insert_many(data[i:i+100]).execute()

print()

Data={
    "users":[],
    'news':[],
}
with open('./minidata_raw_train.txt','r') as f:
    with open('./all_cross_test.txt','w') as f1:
        for lines in f:
            print()
