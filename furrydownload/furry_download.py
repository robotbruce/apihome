
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:04:52 2020

@author: bruceyu1113
"""
import pymysql
import pandas as pd
import sys
from flask import jsonify,request,Flask,render_template, redirect, url_for,flash, send_file,Blueprint
from flask_login import login_required
path = "C:/Users/bruceyu1113/code/API/version/blueprint/recom_api/recom"
sys.path.insert(0, path)
from cache import cache
import db_config
path = "C:/Users/Public/version_control/code/warehouse"
sys.path.insert(0, path)
from FLU import return_xlsx
import io

furry_download = Blueprint('furry_download',__name__,url_prefix='/furry_download')

@furry_download.route('/download')
@login_required
def table():
    return render_template("table_furry.html")


@furry_download.route('/furry_api', methods=['GET'])
@login_required
#    @cache.cached(timeout=300)
def flurry_data():
    flurry_token = request.args.get('flurry_token', None, type = str)
    import_lst = return_xlsx(flurry_token)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    for name, data in import_lst.items():
        data.to_excel(writer,  sheet_name = name, index = False)
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename = 'app成效追蹤報表.csv', as_attachment = True)


