from Recommendation.JGW_Modify.newsExtracter_Package.newsExtracter import Extracter
import pandas as pd
import numpy as np
# from Recommendation.JGW_Modify.test_fsq import user_info_in
from urllib.parse import quote
import urllib.request
import time
import string
import json
from collections import OrderedDict
import re
from tqdm import tqdm

# fsq=user_info_in()
def permid_search( entity_name):
    if (entity_name == None):
        return False
    header = {
        # 'X-AG-Access-Token': "dgKHpotpGLBMkYHDqYHMfqNgG0TkAGd2",
        'X-AG-Access-Token':"8VZ1mNTZ66RyocxHAl4MBP2qirOqYzlC",
        # 'Accept':'application/json,text/plan,"/"',
        # 'Host':'api.thomsonreuters.com'
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    url_path = r'https://api.thomsonreuters.com/permid/search?q=name:'
    url = quote(url_path + entity_name, safe=string.printable)
    req = urllib.request.Request(url, headers=header)
    while (1):
        try:
            text = urllib.request.urlopen(req)
            break
        except Exception as e:
            time.sleep(10)
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

def getUserClick(userID,size,source):
    ifClick = np.random.randint(0, 2, data.values.shape[0])[:size]
    getList = np.random.permutation(data.values)[:size, 0]
    userColumn=np.full((size,1),userID)
    result=np.concatenate((userColumn,getList.reshape(-1,1),ifClick.reshape(-1,1)),axis=1)
    return result

text=permid_search("金蝶")
data=pd.read_csv("./raw_news.csv")
users=[]
for i in range(5):
    users.append(getUserClick(i+1,1000,data.values))
# ifClick=np.random.randint(0,2,data.values.shape[0])
# getList=np.random.permutation(data.values)[:,0]
eneityList,permIdList=[],[]
extracter=Extracter()
extracter.createSubjectModel()
for rows in tqdm(data.values[:10]):
    temp=extracter.extractSubject(rows[1])
    if temp:
        eneityList.append(temp[0][0])
        # tempPerm=permid_search(temp[0][0])
        # if tempPerm:
        #     permIdList.append(tempPerm)
        # else:
        permIdList.append("None")
    else:
        eneityList.append("None")
        permIdList.append("None")
finalData=np.concatenate((data.values[:10],np.array([eneityList,permIdList]).transpose()),axis=1)
pd.DataFrame(finalData).to_csv('test_csv')
for i in range(5):
    pd.DataFrame(users[i]).to_csv('userCLick_'+str(i)+".csv")

pd.DataFrame(users).to_csv('userCLick')

print()