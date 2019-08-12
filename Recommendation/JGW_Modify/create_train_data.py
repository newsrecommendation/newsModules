from peewee import *
from tqdm import trange
import numpy as np
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
result=[]
for x in selector:
    result.append([
        x.user_id, x.news_id.news_title,int(x.if_click),x.news_id.news_entity_permID+":"+x.news_id.news_entity
    ])

pd.DataFrame(result).to_csv('jgw_raw_train.txt',sep='\t',header=False,index=False)
print()