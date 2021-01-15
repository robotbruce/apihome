
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:04:52 2020

@author: bruceyu1113
"""
import pymysql
import pandas as pd
import sys
from flask import request,make_response,render_template,Blueprint
from flask_login import login_required
path = "C:/Users/bruceyu1113/code/API/version/api"
sys.path.insert(0, path)
from cache import cache
import db_config

eccsv_download = Blueprint('eccsv_download',__name__,url_prefix='/ec_table')

@eccsv_download.route('/table')
@login_required
def table():
    return render_template("table.html")
    
  
#################################################
@eccsv_download.route('/ec_data', methods=['GET'])
@login_required
#    @cache.cached(timeout=300)
def aws_news_api():
    mysql = db_config.mysql
    args = request.args
    db_config.gcp_db()
    
    start_date = args.get('start_date') if 'start_date' in args else None
    end_date = args.get('end_date') if 'end_date' in args else None
    
    cache_table = cache.get('cache_data'+str(start_date)+'_'+str(end_date))
    
    if (start_date == None) or (end_date == None):
        if not cache_table:
            print('Not cache')
            insert_NoHave_date = """SELECT * FROM MartServer.EC_Order_Mart where SupplierNumber not in ('I0001','I0007') and dateorder<date(now())"""
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(insert_NoHave_date)          
            rows = cur.fetchall()
            cur.close()
            conn.close() 
            
            frame = pd.DataFrame(rows)
            frame = frame.drop(['idEC_Order_Mart'], axis = 1) 
            frame.columns
            frame = frame.rename(columns={"ShopClass": "館分類","OrderStatus": "訂單狀態","DateOrder": "訂單成立日期","ShoppingCarNumber": "購物車編號","OrderNumber": "訂單編號","SupplierNumber": "供應商廠編","SupplierName": "供應商名稱","ItemLineClass": "線分類","ItemMainclass": "父分類","ItemSubclass": "子分類","ProductNumber": "商品編號","ProductName": "商品名稱","ProductSpecificate": "商品規格","UniPrice": "單價","PurchaseQuantity": "數量","TotalAmout": "總售價","DiscountPriceCilck": "點我再折金額","ActiveCombineName": "組合活動名稱","ActiveCombimePrice": "組合活動金額","UltimatePrice": "末端售價金額","ProductAttribure": "商品屬性","CouponName": "折價券名稱","ComponPrice": "折價券金額","ShoppingCarActiveName": "購物車活動名稱","ShoppingCarActivePrice": "購物車活動金額","DiscountCodeName": "折扣碼名稱","DiscountCodePrice": "折扣碼金額","BonusPointPrice": "紅利點數金額","DiscountUltimatePrice": "折扣總金額","ConsumerPaidAmout": "消費者實付金額","DataPaymentComplete": "付款完成日期","PaymentType": "付款方式","MemberID": "會員mid","MemberEmail": "會員email","MemberGender": "會員性別","MemberAge": "會員年齡","DateInvoiceOpen": "發票開立日期","RecipientAddress": "收件人地區","DateShipping": "出貨日期","DateCancelOrder": "取消單申請日期","CancelOrderReason": "取消單原因","DateReturn": "退貨完成日期","ReturnReason": "退貨原因","PlatformPrice": "平台費","SplitRatio": "分潤比","CgdUniNumber":"賣場流水編號","CgdNumber":"賣場編號","RecipientZip":"收件人郵遞區號","RecipientCity":"收件人城市","RecipientArea":"收件人地址"})
            resp = make_response(frame.to_csv(index=False,encoding='utf_8_sig'))
            resp.headers["Content-Disposition"] = "attachment; filename=ec_data_all.csv"
            resp.headers["Content-Type"] = "text/csv"
            cache_table=resp

            cache_table.status_code=200
            cache.set('cache_all_data',cache_table,timeout=86400)
            return cache_table
        else:
            print('cache_data')
            return cache_table
    else:
        if not cache_table:
            print('Not cache')
        
            start_date_str = "'"+'-'.join([str(''.join(str(start_date)[0:4])),str(''.join(str(start_date)[4:6])),str(''.join(str(start_date)[6:8]))])+"'"
            end_date_str = "'"+'-'.join([str(''.join(str(end_date)[0:4])),str(''.join(str(end_date)[4:6])),str(''.join(str(end_date)[6:8]))])+"'"
            insert_Have_date = """SELECT * FROM MartServer.EC_Order_Mart where SupplierNumber not in ('I0001','I0007') and (date(dateorder) >= %s and date(dateorder) <= %s)and dateorder<date(now());""" % (start_date_str,end_date_str)
            
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(insert_Have_date)          
            rows = cur.fetchall()
            
            frame = pd.DataFrame(rows)
            frame = frame.drop(['idEC_Order_Mart'], axis = 1) 
            frame = frame.rename(columns={"ShopClass": "館分類","OrderStatus": "訂單狀態","DateOrder": "訂單成立日期","ShoppingCarNumber": "購物車編號","OrderNumber": "訂單編號","SupplierNumber": "供應商廠編","SupplierName": "供應商名稱","ItemLineClass": "線分類","ItemMainclass": "父分類","ItemSubclass": "子分類","ProductNumber": "商品編號","ProductName": "商品名稱","ProductSpecificate": "商品規格","UniPrice": "單價","PurchaseQuantity": "數量","TotalAmout": "總售價","DiscountPriceCilck": "點我再折金額","ActiveCombineName": "組合活動名稱","ActiveCombimePrice": "組合活動金額","UltimatePrice": "末端售價金額","ProductAttribure": "商品屬性","CouponName": "折價券名稱","ComponPrice": "折價券金額","ShoppingCarActiveName": "購物車活動名稱","ShoppingCarActivePrice": "購物車活動金額","DiscountCodeName": "折扣碼名稱","DiscountCodePrice": "折扣碼金額","BonusPointPrice": "紅利點數金額","DiscountUltimatePrice": "折扣總金額","ConsumerPaidAmout": "消費者實付金額","DataPaymentComplete": "付款完成日期","PaymentType": "付款方式","MemberID": "會員mid","MemberEmail": "會員email","MemberGender": "會員性別","MemberAge": "會員年齡","DateInvoiceOpen": "發票開立日期","RecipientAddress": "收件人地區","DateShipping": "出貨日期","DateCancelOrder": "取消單申請日期","CancelOrderReason": "取消單原因","DateReturn": "退貨完成日期","ReturnReason": "退貨原因","PlatformPrice": "平台費","SplitRatio": "分潤比","CgdUniNumber":"賣場流水編號","CgdNumber":"賣場編號","RecipientZip":"收件人郵遞區號","RecipientCity":"收件人城市","RecipientArea":"收件人地址"})

            resp = make_response(frame.to_csv(index=False,encoding='utf_8_sig'))
            resp.headers["Content-Disposition"] = "attachment; filename=ec_data_"+str(start_date)+"_"+str(end_date)+".csv"
            resp.headers["Content-Type"] = "text/csv"
            cache_table = resp
            
            cache_table.status_code=200
            cache.set('cache_data'+str(start_date)+'_'+str(end_date),cache_table,timeout=600)
            cur.close()
            conn.close()
            return cache_table
        else:
            print('cache_data')
            return cache_table
