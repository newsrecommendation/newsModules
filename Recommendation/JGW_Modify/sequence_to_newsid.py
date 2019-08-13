from peewee import *
import pandas as pd
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
class user_click(Model):
    click_id=PrimaryKeyField()
    user_id=IntegerField()
    # news_id=IntegerField()
    news_id=ForeignKeyField(news_collection,related_name='news_id')
    if_click=BooleanField()
    class Meta:
        database=db
user_click.bind(db)
news_collection.bind(db)
selector=user_click.select()
data=pd.read_csv("./recom_v1.csv")
result=[[] for i in range(len(data.values))]
for i in trange(len(data.values)):
    clickID=data.values[i][1]
    temp= selector.where(user_click.click_id==clickID+1)[0]
    result[temp.click_id-1]=[temp.news_id.news_title,temp.news_id.news_entity,temp.news_id.news_entity_permID,temp.news_id.news_content]

pd.DataFrame(result).to_csv('clickid_to_news',header=False,index=False)
print()