# from peewee import *
# db = MySQLDatabase("test", host="localhost", port=3306, user="root", passwd="123")
# db.connect()
# class news_collection(Model):
#     news_id=PrimaryKeyField()
#     news_title=TextField()
#     news_entity=TextField()
#     news_entity_permID=TextField()
#     news_content=TextField()
#     class Meta:
#         database=db
# news_collection.bind(db)
# selector=news_collection.select()
import numpy as np
import random
temp=np.full((100,100),0.)
for x1 in range(100):
    for x2 in range(100):
        temp[x1][x2]+= random.random()*0.0000001
for x1 in range(100):
    temp[x1][random.randint(0,8)]=1+(random.random()-0.5)*0.000001
# temp[99][99]=1
print()