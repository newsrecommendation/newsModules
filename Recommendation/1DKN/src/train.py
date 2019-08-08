from dkn import DKN
import tensorflow as tf
import numpy as np
import pandas as pd
from data_loader import read


logs_path = "tensor_logs"


def get_feed_dict(model, data, start, end):
    feed_dict = {model.clicked_words: data.clicked_words[start:end],
                 model.clicked_entities: data.clicked_entities[start:end],
                 model.news_words: data.news_words[start:end],
                 model.news_entities: data.news_entities[start:end],
                 model.labels: data.labels[start:end]}
    return feed_dict

def train(args, train_data, test_data):
    model = DKN(args)
    train_len = 985
    aver_score = np.zeros(train_len)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())
        # tensorboard
        merged_summary_op = tf.summary.merge_all()  # 定义记录运算
        summary_writer = tf.summary.FileWriter(logs_path, graph=tf.get_default_graph())  # 创建写对象

        for step in range(args.n_epochs):
            # training
            start_list = list(range(0, train_data.size, args.batch_size))
            np.random.shuffle(start_list)
            for start in start_list:
                end = start + args.batch_size
                model.train(sess, get_feed_dict(model, train_data, start, end))

            # evaluation
            train_auc,score,summary = model.eval(sess, merged_summary_op, get_feed_dict(model, train_data, 0, train_data.size))
            # test_auc,score,summary = model.eval(sess, merged_summary_op,get_feed_dict(model, test_data, 0, test_data.size))
            # tensorboard
            tf.summary.scalar('score',score)
            summary_writer.add_summary(summary, args.n_epochs * train_data.size + args.batch_size)

            # print('epoch %d    train_auc: %.4f    test_auc: %.4f' % (step, train_auc, test_auc))
            print('epoch %d   train_auc: %.4f' % (step, train_auc))

            aver_score += score
        aver_score /= args.n_epochs
        prop_user2news = pd.DataFrame({'news_id':range(train_len),'prop':aver_score})
        df_userid = read(args.train_file)['user_id']
        df = pd.concat([df_userid, prop_user2news], axis=1)
        print(df.head())
        df = df.groupby('user_id').apply(lambda x: x.sort_values('prop', ascending=False))
        df.to_csv('recom.csv')
