# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:30:01 2020

@author: bruceyu1113
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime

def get_tvbs_news_tag_analysis():
    r = requests.get("http://34.80.91.60:8090/tvbs-news-tag-analysis?$format=json",verify = False)
    list_of_dicts = r.json()
    dfItem = pd.DataFrame.from_records(list_of_dicts)
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

def get_tag_recommend(ARTICLE):
    article = ARTICLE
    dfItem = get_tvbs_news_tag_analysis()
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

#article ='美國人可望在12月11或12日開始接種疫苗。美國政府疫苗負責官員施勞威接受CNN專訪表示，輝瑞藥廠已在上周五向聯邦食品藥物管理局FDA申請緊急授權，而FDA將在於12月10日開會，如果獲得批准，隔天疫苗就可送出，讓美國民眾接受施打。'
#tag1 = get_tag_recommend(article)
