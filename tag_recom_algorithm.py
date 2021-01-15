# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 12:01:27 2020

@author: bruceyu1113
"""

import requests
import pandas as pd
#import time
from collections import Counter

def get_tvbs_Tagdata(DAY):
    day=DAY
    back_tag = requests.get("http://34.80.91.60:8090/aws-news-api-server?day="+str(day),verify = False)
    back_tag_of_dicts = back_tag.json()
    back_tag_of_dfItem = pd.DataFrame.from_records(back_tag_of_dicts)
    return(back_tag_of_dfItem)
    
def get_tag_analys_Tagdata():
    api_tag = requests.get("http://api.analysis.tw/api/tag_json.php?limit=30000",verify = False)
    api_tag_of_dicts = api_tag.json()
    api_tag_dfItem = pd.DataFrame.from_records(api_tag_of_dicts)
    return(api_tag_dfItem)

class editorTag():
    def __init__(self,BACK_TAG_OF_DFITEM):
        self.back_tag_of_dfitem = BACK_TAG_OF_DFITEM
    def tag_matrix(self):
#        clean_content.apply(lambda x : [w for w in jieba.cut(x) if len(w) > 1 and re.compile(r"[A-Z\u4e00-\u9fa5]").findall(w)])
        back_tag = self.back_tag_of_dfitem[['date','tag']]
        back_date_distinct = sorted(back_tag['date'].drop_duplicates().tolist(),reverse = True)
        #back_tag_distinct = list(filter(None,[','.join(back_tag['tag'].tolist())]))
        back_str = ','.join(back_tag['tag'].tolist())
        back_tag_distinct = list(set(list(filter(None,[y.strip() for y in back_str.split(',')]))))
        back_tag_distinct = list(map(lambda x: x.replace("#",""),back_tag_distinct))
        back_tag_distinct = list(set(back_tag_distinct))           
        back_tag_distinct = [w for w in back_tag_distinct if len(w) > 1]
        back_tag_df = pd.DataFrame(back_tag_distinct,columns=['tag'])
        for date in back_date_distinct:
            temp_date_df = ','.join(back_tag[back_tag['date']==date]['tag'].to_list())
            temp_list_uniq =[y.strip() for y in temp_date_df.split(',')]
            temp_list_uniq = list(filter(None,temp_list_uniq))
            temp_list_uniq = list(map(lambda x: x.replace("#",""),temp_list_uniq))
            counter_dict = dict(Counter(temp_list_uniq))
            temp_df = pd.DataFrame(counter_dict.items(),columns = ['tag',date])
            back_tag_df = pd.merge(back_tag_df,temp_df, on = ['tag'],how = 'left')
            back_tag_df = back_tag_df.fillna(0)
        return(back_tag_df)              
    def editor_tag_summary(self):
        tag_summary = pd.DataFrame()
        back_tag_df = self.tag_matrix()
        cols = back_tag_df.columns.drop('tag')
        back_tag_df[cols] = back_tag_df[cols].apply(pd.to_numeric, errors='coerce')
        tag_table_z = back_tag_df.mask(back_tag_df == 0).drop(['tag'], 1)
        tag_summary["tag"] = back_tag_df['tag']
        tag_summary["allcounter"] = back_tag_df.sum(axis=1)
        tag_summary["max_date"]  = back_tag_df.iloc[:,2:].idxmax(axis=1).map(lambda x: x.replace('_x',''))
        tag_summary['max_count'] = back_tag_df.max(axis=1)
        tag_summary = tag_summary.assign(last_date=tag_table_z.apply(pd.Series.first_valid_index, 1),start_date=tag_table_z.apply(pd.Series.last_valid_index, 1))
        return(tag_summary)
    
#if __name__=='__main__':
#    now = time.time()
#    back_tag_of_dfItem = get_tvbs_Tagdata()
#    later = time.time()
#    difference = int(later - now)
#    print("get api time cost: %d Sec" %(difference))
#    
#    now = time.time()
#    tag_summary = editorTag(back_tag_of_dfItem).editor_tag_summary()
#    later = time.time()
#    difference = int(later - now)
#    print("tag Summary time cost: %d Sec" %(difference))
