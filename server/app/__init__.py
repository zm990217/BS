from flask import Flask
from flask_cors import CORS
import pymysql

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import mysqlconnector

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:zm348646486@127.0.0.1:3306/sswj'
app.config['SQLALCHEMY_MODIFICATIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/sswj/api/*": {"origins": "*"}})

from views import views
app.register_blueprint(views)