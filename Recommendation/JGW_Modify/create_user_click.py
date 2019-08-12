from peewee import *
import random
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
    news_id=IntegerField()
    if_click=BooleanField()
    class Meta:
        database=db

user_click.bind(db)
news_collection.bind(db)
userClick=[]
for userID in range(5):
    selector = news_collection.select().where(news_collection.news_entity_permID != "None")
    currentUserClick={}
    for x in selector:
        temp={
            "user_id":userID,
            "news_id":x.news_id,
            "if_click":bool(random.randint(0,1))
        }
        userClick.append(temp)

with db.atomic():
    for i in trange(0, len(userClick), 100):
        # news_collection.create(**tempInsert)
        user_click.insert_many(userClick[i:i + 100]).execute()