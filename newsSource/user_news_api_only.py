# coding:utf-8
import random
import os
import urllib.request
from urllib.parse import quote
import string
import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import re
from Things_Define_MainNER_Triple.newsExtracter import Extracter

'''
本模块需要初始化
整体程序之前调用init，具体例子见main函数内
使用User.outline()，将会返回的代码形式：
    [userid, title , permid , entity]
    其中userid为%d形式，其他均为str

    例：[10330, '金蝶纯利增长达34%创四年同期新高', '4295871245', '金蝶']
'''

# [userid,newstitle,PermID:标题的实体]

APItoken = 'dgKHpotpGLBMkYHDqYHMfqNgG0TkAGd2'
global newsid


class init():
    def __init__(self):
        global newsid
        newsid = 644000


class user_info_in():
    def permid_search(self, entity_name):
        header = {
            'X-AG-Access-Token': APItoken,
            # 'Accept':'application/json,text/plan,"/"',
            # 'Host':'api.thomsonreuters.com'
        }
        url_path = r'https://api.thomsonreuters.com/permid/search?q=name:'
        url = quote(url_path + entity_name, safe=string.printable)
        req = urllib.request.Request(url, headers=header)
        text = urllib.request.urlopen(req)
        text = text.read().decode('utf-8')
        # text=BeautifulSoup(text)
        text = json.loads(text, object_pairs_hook=OrderedDict)
        text = text["result"]["organizations"]["entities"]
        if (text == []):
            print("False")
            return False
        last = text[0]['@id']
        permid = re.findall(r'https://permid.org/\d-(\d+)', last)
        return permid[0]

    def newsfile(self):
        for i in range(self.newsid, 800000):
            path = '股票/'
            if (os.path.exists(path + str(i) + '.txt')):
                self.newsid = i + 1
                nf = open(path + str(i) + '.txt', 'r')
                title = nf.readlines()[0].replace('\n', '')
                return title
        return "without newsfile"

    def search_news(self, control):
        '''
        if control==1:
            返回数据库新闻
        if control==2:
            返回及时新闻
        :param control:
        :return:
        '''
        lines = []
        if control == 1:
            nf = self.newsfile()
            if (nf == "without newsfile"):
                control = 2
            else:
                return nf
        if control == 2:  # 可能接外部接口
            return lines

    def search_news_entity(self, news):
        # entity=extracter.extractClass(self.news) #事件定义
        entity = self.extracter.extractSubject(news)  # 可以批量处理
        entity = entity[0][0]
        return entity

    def outline(self, news_number=1, control=1):
        self.news_number = news_number
        self.news = self.search_news(control)
        self.news_entity = self.search_news_entity(self.news)
        # print([self.userid,self.news,self.news_entity])
        self.permid = self.permid_search(self.news_entity)
        return [self.userid, self.news, self.permid, self.news_entity]

    def write_txt(self):
        print("userid\ttitle\tis_click\tpermid:entity")
        return

    def __init__(self):
        global newsid
        self.newsid = newsid
        self.userid = 10330
        self.control = 1
        self.extracter = Extracter()
        # self.extracter.createClassModel()
        self.extracter.createSubjectModel()


if __name__ == "__main__":
    init()
    User = user_info_in()
    print(User.outline())
    print(User.outline())
