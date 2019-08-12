from peewee import *
import pandas as pd
from tqdm import tqdm
from tqdm import trange
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



path='./news_user_Data/'
raw_data=pd.read_csv(path+'test_csv')
data=[]
for x in tqdm(raw_data.values):
    data.append({
        "news_id":x[1],
        "news_title":x[2],
        "news_content":x[3],
        "news_entity":x[4],
        "news_entity_permID":x[5]
    })
with db.atomic():
    for i in trange(0, len(data), 100):
        # news_collection.create(**tempInsert)
        news_collection.insert_many(data[i:i + 100]).execute()
news_collection.bind(db)


print()