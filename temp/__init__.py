# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:08:22 2021

@author: bruceyu1113
"""

from flask import Flask
from api.health import api as health_api
from api.supertaste import api as supertaste_api
from api.news import api as news_api
#from cache import cache
#from api.news import cache
from flask_cache import Cache

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["JSON_AS_ASCII"] = False
    app.config['CACHE_TYPE']='simple'
#    cache = Cache(app)
    cache.init_app(app)
    app.register_blueprint(health_api)
    app.register_blueprint(supertaste_api)
    app.register_blueprint(news_api)
    return(app)


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0",port=50,debug=True, use_reloader=False)