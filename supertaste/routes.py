# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:13:45 2021

@author: bruceyu1113
"""
from flask import Blueprint


supertaste = Blueprint('supertaste',__name__,url_prefix='/supertaste')

@supertaste.route('/getdata')
def getdata():
    return{'supertaste': 'value'}