# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:30:01 2020

@author: bruceyu1113
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime

class cache_tag_table:
    def __init__(self,domain,GSC):
        self.domain = domain
        self.gsc = GSC
    def get_table(self):
        r = requests.get(f"http://34.80.91.60:5050/{self.domain}/tag_score_table?$format=json&gsc={self.gsc}",verify = False)
        list_of_dict = r.json()
        dfItem = pd.DataFrame.from_records(list_of_dict)
        return(dfItem)

def make_score(DFITEM):
    dfItem = DFITEM
    now = datetime.now().date()
    strToDcolumn = ['last_date','max_date','start_date']
    for col in strToDcolumn:
        dfItem[col] = pd.to_datetime(dfItem[col]).dt.date
    
    dfItem['score'] = (np.sqrt(dfItem['allcounter'])/((np.log10((abs(dfItem['last_date'] - dfItem['start_date']).dt.days) + 1)/np.log10(100)) + 1))*(dfItem['max_count']/(abs(now - dfItem['max_date']).dt.days)+1)
    dfItem.sort_values(by=['score'],ascending=False,inplace=True)
    return(dfItem)

def get_tag_recommend(domain,ARTICLE,GSC):
    article = ARTICLE
    gsc = GSC
    dfItem = cache_tag_table(domain,gsc).get_table()
    dfItemScore = make_score(dfItem)
    temp_list = []
    for i in dfItem['tag']:
        if i in article:
            temp_list.append(i)
    sc_df = dfItemScore[dfItemScore['tag'].isin(temp_list)][['tag','score']]       
    sc_df.sort_values(by=['score'],ascending=False,inplace=True)
    sc_df['score'] = sc_df.score.round(3)
    sc_df.reset_index(drop = True,inplace=True)
    tag_list =sc_df['tag'].to_list()[:20]
    tag_str = ','.join(tag_list)
    return(tag_str)

#health_tagtable = cache_tag_table('health').get_table()
#get_tag_recommend('news','在治療方面，林俊宏說明，子宮內膜癌確診後採手術治療為主，傳統是開腹式手術，微創手術有腹腔鏡或達文西，儘管病人的腫瘤僅限於子宮內，但在沒有生育的考量下，醫師會建議切除子宮、卵巢、輸卵管、骨盆腔、主動脈淋巴腺等，再依照病理化驗的結果，確立病人的癌症期數，以準確預後和確定適當的治療方法。')

#article ='美國人可望在12月11或12日開始接種疫苗。美國政府疫苗負責官員施勞威接受CNN專訪表示，輝瑞藥廠已在上周五向聯邦食品藥物管理局FDA申請緊急授權，而FDA將在於12月10日開會，如果獲得批准，隔天疫苗就可送出，讓美國民眾接受施打。'
#tag1 = get_tag_recommend(article)
