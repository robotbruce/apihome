# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 17:32:29 2020

@author: bruceyu1113
"""


##reload_news_cache
import requests
#from datetime import datetime

##d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'1:00', '%Y-%m-%d%H:%M')
##print(d_time)
##d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'1:02', '%Y-%m-%d%H:%M')
##print(d_time1) 

#n_time = datetime.datetime.now()

#if n_time >= d_time and n_time<=d_time1:
#    print('in time')
#else:
#    print('登愣')
#    pass

#news_cache
r1 = requests.get("http://34.80.91.60:5050/news/article_cache",verify = False) ##cache新聞table
print(r1.status_code)
r2 = requests.get("http://34.80.91.60:5050/news/tag_score_table",verify = False)##cache 標籤分數
print(r2.status_code)
r3 = requests.get("http://34.80.91.60:5050/news/news-recom-batch-update",verify = False)##cache 批次更新
print(r3.status_code)

#supertaste_cache
r4 = requests.get("http://34.80.91.60:5050/supertaste/tag_score_table",verify = False)##cache 標籤分數
print(r4.status_code)

#woman_cache
r5 = requests.get("http://34.80.91.60:5050/woman/tag_score_table",verify = False)##cache 標籤分數
print(r5.status_code)

#health_cache
r6 = requests.get("http://34.80.91.60:5050/health/tag_score_table",verify = False)##cache 標籤分數
print(r6.status_code)