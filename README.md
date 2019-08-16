## 基于知识图谱的金融新闻推荐系统

#### 主要部分：

NewsSource、Recommendation、FrontEnd、BackEnd、DataBase

#### 部署流程：
0. 若仅需要展示使用已完成的展示数据，直接进入BackEnd/flask_blue_test中运行flask run —host=0.0.0.0，
进入FrontEnd/vuecli中运行npm run serve并访问0.0.0.0:8080即可

1. 将DataBase文件夹中csv导入数据库（含四个表）

2. 在Recommendation文件夹进行推荐分析

   1. 若需要使用新数据、则依次使用JGW_Modify中create_user_click、create_train_data、create_class_triple、分别创建用户点击情况（存入数据库中）、与文件jgw_raw_train.txt、jgw_classtriples.txt
   2. 使用news/news_preprocess根据jgw_raw_train生成test.txt train.txt jgw_enity2index jgw_word_embeddings
   3. 使用kg/prepare_data_for_transx根据classTriple.txt生成jgw_triple2id jgw_relation2id jgw_enity2id
   4. 使用kg/fast_trans_x/transE/transE.cpp生成jgw_transe_relation2vec_50 jgw_transe_enity2vec_50（其中的50代表维度可自行修改）
   5. 使用kg/kg_preprocess生成jgw_enity_embeddings_TransE_50.npy jgw_context_embeddings_TransE_50.npy
   6. (我生成的Jgw_data保存了训练时的中间结果，可供参照)
   7. 使用main进行训练，得出结果recom.csv，即每个用户对每个clickid所指向的新闻的预测概率
   8. 使用JGW_Modify中的sequence_to_newsid生成clickid_to_news

3. 使用BackEnd创建后台

   1. 修改appnews/views中click_to_news路径指向新的click_to_news
   2. 在flask_blue_test中运行flask run —host=0.0.0.0

4. 使用FrontEnd创建前台

   1. 修改vuecli/src/components中newsList中的请求新闻地址为真实的地址（Ln 121）                 

      url:"http://0.0.0.0:5000/appnews/get_news_jgw/"+this.userID.toString()+"/",

   2. 修改对于新闻之间联系与新闻倾向的随机处理（需要导入数据替换展示用的伪随机部分）

   3. 在vuecli文件夹下运行npm run serve，随后访问0.0.0.0:8080即可访问