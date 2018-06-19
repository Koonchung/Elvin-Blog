# -*- coding: utf-8 -*-
# author: Chan

# MySQL	            mysql+pymysql://username:password@hostname/database
# Postgres	        postgresql://username:password@hostname/database
# SQLite(Unix)	    sqlite:////absolute/path/to/database
# SQLite(Windows)	sqlite:///c:/absolute/path/to/database

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'path_to_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), unique=False)
    content = db.Column(db.String(100), unique=False)
    author = db.Column(db.String(32), unique=False)
    time = db.Column(db.String(30), nullable=True,
                     default=datetime.date.today())

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author


class User(db.Model):
    __tablename__ = 'userdata'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
