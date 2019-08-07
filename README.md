# newsModules

20190807 接新闻训练数据交接文档:
1、发给推荐模型的新闻数据要求train的字段及格式为：[user_id, news_id, news_title , is_clicked, permid: entity]，  
train中总共包含2w条左右新闻，400个左右用户的点击历史,每个用户点击过2w条中的20-100篇新闻；  
news_title需要能概括新闻内容；  
entity尽量保证是news_title中的单词，并且permid是entity在路福特给出的KG中的对应entity的id,如果KG中不存在该entity,则permid=-1  
2、test字段及格式为:[news_id, news_title,permid: entity_name]  
输入的新闻为2w条左右；  
news_id是数据库的key  
