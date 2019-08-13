from peewee import *
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
news_collection.bind(db)
selector=news_collection.select()
