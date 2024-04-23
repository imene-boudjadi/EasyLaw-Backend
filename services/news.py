from flask import request
from ..models.news import  News
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
# import jwt
# from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from .. import db



def get_all_news():
    news = News.query.all()
    return news

def get_one_new(id):
    new = News.query.filter_by(idNews=id).first()
    return new