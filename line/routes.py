# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 17:48:34 2020

@author: bruceyu1113
"""

from flask import jsonify,request,Blueprint
import requests,json

lineapi = Blueprint('lineapi',__name__,url_prefix='/linenNotify')
@lineapi.route('/getdata')
def getdata():
    return{'news': 'value'}
@lineapi.route("/call")
def callback():
    return jsonify({'data' : request.url})

@lineapi.route("/LineNotify-news-error",methods=['GET'])
def notify_news_error_message():
    ip_address = request.args.get('ip_address', None, type = str)
    message = request.args.get('message', None, type = str)
    picURI = request.args.get('picURI', None, type = str)
    request_url = request.args.get('request_url',None, type = str)
    try:
#        if message != None:
            #取得發送目標token
        with open(f'\\Users\\Public\\Documents\\token\\linetoken.json') as json_file: 
            tokenData = json.load(json_file) 
        token = tokenData['shiaubu_ErrorMessage_datateam']
        #傳送訊息
        headers = { "Authorization": "Bearer " + token}
    #               "Content-Type" : "application/x-www-form-urlencoded"}
        files = {'imageFile':open(picURI,'rb')} if picURI else None
        payload={'message':f"\nrequest ip address:{ip_address}\n\nerror type:{message}\n\nrequest_url:{request_url}"}
        res = requests.post('https://notify-api.line.me/api/notify',data=payload,headers=headers,files = files)
        status_string = str(res.status_code)
        print(res.status_code)
    except Exception as e:
        status_string = str(e)
        print(e)
    return jsonify({"status":f"{status_string}"})