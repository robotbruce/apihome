import requests
import numpy as np
import pandas as pd
import datetime


def get_new_record(nid, get_type, title, tag, summary, date):
    
    nnid = nid
    nget_type = get_type
    ntitle = title
    ntag = tag
    nsummary = summary
    ndate = date
    
    new_record = [nnid, nget_type, ntitle, ntag, nsummary, ndate]
    new_record = pd.DataFrame(new_record).T
    new_record.columns = ['nid', 'get_type', 'title', 'tag', 'summary', 'date']
    
    return new_record

#new_record = get_new_record(nid = 9999999, 
#                            get_type = 4, 
#                            title = '聲稱賓州領先　川普嗨喊「已經贏了」：他不可能追過我', 
#                            tag = '美國大選,美選,川普,拜登,關鍵搖擺州,46張票', 
#                            summary = '全球矚目的2020美國總統大選正在如火如荼展開，有3個搖擺州成為影響大選的關鍵。外媒消息指出，密西根州、賓夕法尼亞州及威斯康辛州擁有46張選舉人票，但恐怕不會開票日當日有結果。', 
#                            date = datetime.date(2020, 11, 4))
#
#new_record = get_new_record(nid = 9999999, 
#                            get_type = 4, 
#                            title = '測試標題', 
#                            tag = 'ai技術', 
#                            summary = '測試內容', 
#                            date = datetime.date(2020, 12, 2))
#
#new_record = get_new_record(nid = 9999999, 
#                            get_type = 11, 
#                            title = '測試標題', 
#                            tag = '煞車失靈,車禍,遊覽車', 
#                            summary = '測試內容', 
#                            date = datetime.date(2020, 12, 2))


def request_aws_news_api():
    
    request_url = 'http://34.80.91.60:8090/aws-news-api-server?day=91'
    aws_news_api = requests.get(request_url, verify = False)
    aws_news_api_lt = aws_news_api.json()
    rd0 = pd.DataFrame(aws_news_api_lt)
    
    return rd0

#rd0 = request_aws_news_api()


def prepare_raw_data(rd0, new_record):
    
    rd0_p = rd0
    new_record_p = new_record
    
    rd = rd0_p.loc[:, ['nid', 'get_type', 'title', 'tag', 'summary', 'date']].copy()
    rd = rd.append(new_record_p)
    
    rd = rd[(rd['get_type'] != 8)]
    rd = rd[rd['title'].str.find('快訊／') == -1]
    
    rd['tag'] = rd['tag'].replace('', '999')
    rd['tag'] = rd['tag'].str.lower()
    rd['tag'] = rd['tag'].str.replace('#', '')
    rd['tag'] = rd['tag'].str.replace('\+0', '"+0"')
    
    rd['date'] = pd.to_datetime(rd['date']).dt.date
    
    rd['new_index'] = range(0, len(rd))
    rd = rd.set_index('new_index', 'Index')
    
    return rd

#rd = prepare_raw_data(rd0, new_record)




def get_News_Recommend_idGroup(rd, new_record):
    
    rd_p = rd
    new_record_p = new_record
    
    for j in range(len(rd_p)-1, len(rd_p)):
        if rd_p.loc[j, 'tag'] == '999':
            continue
        j_dict = rd_p.loc[j, :].to_dict()
        rd_match = rd_p.copy()
        
        if j_dict['get_type'] == 11:
            rd_match = rd_match[rd_match['get_type'] == 11]
        
        tag_sum = j_dict['tag'].count(',') + 1
            
        for i in range(0, tag_sum):
            tags = j_dict['tag'].split(',')[i]
            rd_match['tag'+str(i+1)] = np.where(rd_match['tag'].str.find(tags) >= 0, 1, 0)
            
        tags_col = range(len(rd_p.columns), len(rd_match.columns))
        rd_match['tag_sum'] = rd_match.iloc[:, tags_col].sum(axis = 1)
        rd_match = rd_match[rd_match['tag_sum'] >= 1]
        
#        a = [x for x in j_dict['tag'].split(',')]
        b = (x for x in rd_match['tag'])
        c = (x.split(',') for x in b)
        d = (list(filter(lambda y: y in j_dict['tag'].split(','), x)) for x in c)
        e = (len(x) for x in d)
        
        tag_num = pd.DataFrame(e, columns = ['tag_num'], index = rd_match.index)
        rd_match = rd_match.merge(tag_num, how = 'left', left_index = True, right_index = True)
        rd_match = rd_match[rd_match['tag_num'] >= 1]
        
        rd_match['date_diff'] = abs(rd_match['date'] - j_dict['date']).dt.days    
        rd_match['specified_type'] = np.where(rd_match['get_type'].isin([4, 12, 6]), 0.1, 0)
            
        rd_match['score'] = (rd_match['tag_num'] + rd_match['specified_type']/(rd_match['tag_num'] + 1)) * 1/(np.log10(rd_match['date_diff'] + 1)/np.log10(100) + 1)
        rd_match_a = rd_match[rd_match['nid'] == j_dict['nid']]
        rd_match_b = rd_match[rd_match['nid'] != j_dict['nid']].sort_values('score', ascending = False).head(10)
        rd_match_recom = rd_match_a.append(rd_match_b)
#        rd_match_recom = rd_match.sort_values('score', ascending = False).head(11)
        rd_match_recom = rd_match_recom.loc[:, ['nid', 'get_type', 'title', 'tag', 'summary', 'date']]
        rd_match_recom['new_index'] = range(0, len(rd_match_recom))
        rd_match_recom = rd_match_recom.set_index('new_index', 'Index')
        
        if len(rd_match_recom) < 2:
                id_group = ''
        else:
            for k in range(1, len(rd_match_recom)):
                id_group = ','.join([str(x) for x in rd_match_recom.loc[1:, 'nid'].tolist()])
                
        nid = j_dict['nid']
        recom_nid = nid, id_group
        recom_nid = pd.DataFrame(recom_nid).T
        recom_nid.columns = ['nid', 'recom_nid']
        
    newRecord_recom_nid = new_record_p.merge(recom_nid, how = 'left', on = 'nid')
#    newRecord_recom_nid['recom_nid'] = newRecord_recom_nid['recom_nid'].fillna('')
#    newRecord_recom_nid['tag'] = newRecord_recom_nid['tag'].replace('999', '')
    
    return newRecord_recom_nid

#newRecord_recom_nid = get_News_Recommend_idGroup(rd, new_record)




def update_News_Recommend_last1(nid, get_type, title, tag, summary, date):
    
    new_record = get_new_record(nid, get_type, title, tag, summary, date)
    
    if new_record.loc[0, 'tag'] == None or new_record.loc[0, 'tag'] == '' or new_record.loc[0, 'get_type'] == 8:
        id_group = ''
        recom_nid = pd.DataFrame([new_record.loc[0, 'nid'], id_group]).T
        recom_nid.columns = ['nid', 'recom_nid']
        newRecord_recom_nid = new_record.merge(recom_nid, how = 'left', on = 'nid')
        
    else:
        rd0 = request_aws_news_api()
        rd = prepare_raw_data(rd0, new_record)
        newRecord_recom_nid = get_News_Recommend_idGroup(rd, new_record)
        
    return new_record, newRecord_recom_nid

#new_record, newRecord_recom_nid = update_News_Recommend_last1(nid = 9999999, 
#                            get_type = 4, 
#                            title = '聲稱賓州領先　川普嗨喊「已經贏了」：他不可能追過我', 
#                            tag = '美國大選,美選,川普,拜登,關鍵搖擺州,46張票', 
#                            summary = '全球矚目的2020美國總統大選正在如火如荼展開，有3個搖擺州成為影響大選的關鍵。外媒消息指出，密西根州、賓夕法尼亞州及威斯康辛州擁有46張選舉人票，但恐怕不會開票日當日有結果。', 
#                            date = datetime.date(2020, 11, 4))
#
#new_record, newRecord_recom_nid = update_News_Recommend_last1(nid = 9999999, 
#                            get_type = 4, 
#                            title = '測試標題', 
#                            tag = 'ai技術', 
#                            summary = '測試內容', 
#                            date = datetime.date(2020, 12, 2))
#
#new_record, newRecord_recom_nid = update_News_Recommend_last1(nid = 9999999, 
#                            get_type = 11, 
#                            title = '測試標題', 
#                            tag = '煞車失靈,車禍,遊覽車', 
#                            summary = '測試內容', 
#                            date = datetime.date(2020, 12, 2))

