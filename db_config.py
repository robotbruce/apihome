from flaskext.mysql import MySQL
from flask import Flask
import json

with open(f"C:\\Users\\Public\\Documents\\db_config\\db_info.json") as json_file: 
    db_info = json.load(json_file) 
 

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
def gcp_db():
    app.config['MYSQL_DATABASE_USER'] = db_info['gcp']['username']
    app.config['MYSQL_DATABASE_PASSWORD'] = db_info['gcp']['password']
    app.config['MYSQL_DATABASE_DB'] = db_info['gcp']['db']
    app.config['MYSQL_DATABASE_HOST'] = db_info['gcp']['host']
    mysql.init_app(app)
    

def aws_db():
    app.config['MYSQL_DATABASE_USER'] = db_info['aws']['username']
    app.config['MYSQL_DATABASE_PASSWORD'] = db_info['aws']['password']
    app.config['MYSQL_DATABASE_DB'] = db_info['aws']['db']
    app.config['MYSQL_DATABASE_HOST'] = db_info['aws']['host']
    mysql.init_app(app)
