# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 12:22:05 2021

@author: bruceyu1113
"""
from flask import Flask
import sys
import json
from flask_login import LoginManager ,UserMixin

path = "C:\\Users\\bruceyu1113\\code\\API\\version\\api"
sys.path.insert(0, path)
from cache import cache

def read_loginList():
    with open(f"C:\\Users\\Public\\Documents\\login_list\\login.json") as json_file:
        users = json.load(json_file)
    return(users)

def query_user(username):
    users = read_loginList()
    for user in users.values():
        if username == user['username']:
            return user

class User(UserMixin):
    pass

def create_app():
    app = Flask(__name__)
    app.secret_key = 'somesecretkeythatonlyishouldknow'
    app.config["DEBUG"] = True
    app.config["JSON_AS_ASCII"] = False
    app.config['CACHE_TYPE']='simple'

    cache.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'ec_table_auth.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Access denied.'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        if query_user(username) is not None:
            curr_user = User()
            curr_user.username = username
        return curr_user

    from health.routes import health
    from supertaste.routes import supertaste
    from woman.routes import woman
    from news.routes import news
    from line.routes import lineapi
    from ec.routes import ec

    from downloadcsv.ectable_download import eccsv_download
    from downloadcsv.auth import auth

    from furrydownload.furry_download import furry_download
    from furrydownload.auth import furry_auth

    app.register_blueprint(health)
    app.register_blueprint(supertaste)
    app.register_blueprint(woman)
    app.register_blueprint(news)
    app.register_blueprint(lineapi)
    app.register_blueprint(ec)

    app.register_blueprint(eccsv_download)
    app.register_blueprint(auth)

    app.register_blueprint(furry_download)
    app.register_blueprint(furry_auth)

    return(app)


if __name__ == '__main__':
    # from flask_cache import Cache
    app = create_app()
    app.run(host="0.0.0.0",port=5050,debug=True, use_reloader=False)

