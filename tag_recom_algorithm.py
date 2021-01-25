# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 12:01:27 2020

@author: bruceyu1113
"""

import requests
import pandas as pd
#import time
from collections import Counter

class cache_article_table:
    def __init__(self,domain):
        self.domain = domain
    def get_aws_table_cache(self,DAY):
        day=DAY
        api_domain = self.domain
        back_tag = requests.get(f"http://34.80.91.60:5050/{api_domain}/article_cache?day={day}",verify = False)
        back_tag_of_dicts = back_tag.json()
        back_tag_of_dfItem = pd.DataFrame.from_records(back_tag_of_dicts)
        return(back_tag_of_dfItem)

#def get_tvbs_Tagdata(DAY):
#    day=DAY
#    back_tag = requests.get("http://34.80.91.60:5050/news/article_cache?day="+str(day),verify = False)
#    back_tag_of_dicts = back_tag.json()
#    back_tag_of_dfItem = pd.DataFrame.from_records(back_tag_of_dicts)
#    return(back_tag_of_dfItem)
#
#def get_health_Tagdata(DAY):
#    day=DAY
#    back_tag = requests.get("http://34.80.91.60:5050/health/article_cache?day="+str(day),verify = False)
#    back_tag_of_dicts = back_tag.json()
#    back_tag_of_dfItem = pd.DataFrame.from_records(back_tag_of_dicts)
#    return(back_tag_of_dfItem)
    
def get_tag_analys_Tagdata():
    api_tag = requests.get("http://api.analysis.tw/api/tag_json.php?limit=30000",verify = False)
    api_tag_of_dicts = api_tag.json()
    api_tag_dfItem = pd.DataFrame.from_records(api_tag_of_dicts)
    return(api_tag_dfItem)

def combine_gsc(domain,back_tag):
    gsc_health = requests.get(f"http://34.80.91.60:5050/{domain}/google_scarch_console_tag")
    gsc_table = gsc_health.json()
    gsc_tag_health = pd.DataFrame.from_records(gsc_table)
    gsc_tag_health['nid'] = gsc_tag_health['nid'].apply(pd.to_numeric, errors='coerce')
    back_tag_df = pd.merge(back_tag,gsc_tag_health, on = ['nid'],how = 'left')
    back_tag_df['tag'] = back_tag_df[['tag', 'search_content']].apply(lambda x: ','.join(x[x.notnull()]), axis = 1)
    back_tag_df['tag'] = back_tag_df['tag'].apply(lambda x: ','.join(set(x.split(','))))
    back_tag_df = back_tag_df.loc[:, back_tag_df.columns != 'search_content']
    return(back_tag_df)

class editorTag():
    def __init__(self,domain,BACK_TAG_OF_DFITEM,GSC):
        self.back_tag_of_dfitem = BACK_TAG_OF_DFITEM
        self.domain = domain
        self.gsc = GSC
    def tag_matrix(self):
        if self.domain != 'news' and self.gsc == 'Y':
            back_tag = combine_gsc(self.domain,self.back_tag_of_dfitem)
        elif self.domain == 'news' or self.gsc == 'N':
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
        
#    a = back_tag_of_dfItem.copy()
#    a.
    
    
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
