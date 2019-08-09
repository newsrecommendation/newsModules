import csv

news_id_list = []
msg = {}
user_id = 1
# with open('/Users/kelang-tian/Desktop/deecamp/git_news/BackEnd/flask_blue_test/recom.csv', 'rt',
#           encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         #print(row['user_id'])
#         if row['user_id'] == str(user_id):
#             news_id_list.append(row['news_id'])
#             print(2222)
#         #print(111)
#         msg = {user_id: news_id_list}
#
#     print(msg)

news_list = []
with open('minidata_raw_train.txt', 'rt', encoding='utf-8') as newsfile:
    lines = newsfile.readlines()
    index = 0
    num = 0
    result = lines[0].split("\t")
    print(result)
    #
    # for line in lines:
    #     print(line.split(" "))



# with open('minidata_raw_train.txt', 'rt', encoding='utf-8') as newsfile:
#     reader_news = csv.DictReader(newsfile)
#
#     index = 0
#     num = 0
#     for row in reader_news:
#         if str(index) in news_id_list:
#             news_list.append(row)
#             num += 1
#         index += 1
#     msg = {num: news_list}
#     return json.dumps(msg, ensure_ascii=False)