import logging
from flask import Flask, redirect, url_for, g
from flask_appbuilder.security.mongoengine.manager import SecurityManager
from flask_appbuilder import AppBuilder
from flask_mongoengine import MongoEngine
from flask_appbuilder.views import IndexView
from flask_appbuilder.baseviews import expose
from pymongo import MongoClient
from .api import UserApi

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)

client = MongoClient('localhost', 27017)
db_client = client.mydb

class MyIndexView(IndexView):
    @expose('/')
    def index(self):
        user = g.user

        if user.is_anonymous:
            return redirect(url_for('AuthDBView.login'))
        else:
            return redirect(url_for('UserDBModelView.list'))
appbuilder = AppBuilder(app, security_manager_class=SecurityManager, indexview=MyIndexView)
appbuilder.add_api(UserApi)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    

from app import views

