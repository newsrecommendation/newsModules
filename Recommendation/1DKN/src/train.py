from dkn import DKN
import tensorflow as tf
import numpy as np
import pandas as pd
from data_loader import read


def get_feed_dict(model, data, start, end):
    feed_dict = {model.clicked_words: data.clicked_words[start:end],
                 model.clicked_entities: data.clicked_entities[start:end],
                 model.news_words: data.news_words[start:end],
                 model.news_entities: data.news_entities[start:end],
                 model.labels: data.labels[start:end]}
    return feed_dict

def train(args, train_data, test_data):
    model = DKN(args)
    aver_score = np.zeros(462)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())

        for step in range(args.n_epochs):
            # training
            start_list = list(range(0, train_data.size, args.batch_size))
            np.random.shuffle(start_list)
            for start in start_list:
                end = start + args.batch_size
                model.train(sess, get_feed_dict(model, train_data, start, end))

            # evaluation
            # train_auc = model.eval(sess, get_feed_dict(model, train_data, 0, train_data.size))
            test_auc,score = model.eval(sess, get_feed_dict(model, test_data, 0, test_data.size))
            # print('epoch %d    train_auc: %.4f    test_auc: %.4f' % (step, train_auc, test_auc))
            print('epoch %d   test_auc: %.4f' % (step, test_auc))

            aver_score += score
        aver_score /= args.n_epochs
        prop_user2news = pd.DataFrame({'news_id':range(462),'prop':aver_score})
        df_userid = read(args.test_file)['user_id']
        df = pd.concat([df_userid,prop_user2news], axis=1)
        df = df.groupby('user_id').apply(lambda x: x.sort_values('prop', ascending=False))
        df.to_csv('recom.csv')
