from flaskext.mysql import MySQL
from flask import Flask
app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
def gcp_db():
    app.config['MYSQL_DATABASE_USER'] = 'TVBS_NM'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'frNsX7V@P@4mRg#8'
    app.config['MYSQL_DATABASE_DB'] = 'MartServer'
    app.config['MYSQL_DATABASE_HOST'] = '10.33.0.3'
    mysql.init_app(app)
    

def aws_db():
    app.config['MYSQL_DATABASE_USER'] = 'tvbs'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'tvbstvbs'
    app.config['MYSQL_DATABASE_DB'] = 'tvbs_news_v4'
    app.config['MYSQL_DATABASE_HOST'] = 'db41-ro-tvbs-aurora.clwuef820xta.ap-northeast-1.rds.amazonaws.com'
    mysql.init_app(app)
