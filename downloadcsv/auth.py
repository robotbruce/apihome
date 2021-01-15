# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:20:51 2021

@author: bruceyu1113
"""

from flask_login import UserMixin,login_user
from flask import request,render_template, redirect, url_for,flash,Blueprint
import json

auth = Blueprint('auth',__name__,url_prefix='/auth')

class User(UserMixin):
    pass

def query_user(username):
    with open(f"C:\\Users\\Public\\Documents\\login_list\\login.json") as json_file: 
        users = json.load(json_file) 
    for user in users.values():
        if username == user['username']:
            return user  

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('username')
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:

            curr_user = User()
            curr_user.id = user_id

            # 通過Flask-Login的login_user方法登入使用者
            login_user(curr_user)
            return redirect(url_for('eccsv_download.table'))
        flash('Wrong username or password!')

    # GET 請求
    return render_template('login.html')

