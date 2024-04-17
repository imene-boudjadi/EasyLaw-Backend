# services.py

from flask import request
from ..models import  Law
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
# import jwt
# from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from .. import db


def get_all_laws():
    laws = Law.query.all()

    return laws


def get_all_laws_with_sum():
    laws = Law.query.all()

    total_sum = db.session.query(func.sum(Law.num_jarida)).scalar()

    return {
        "data": laws,
        "sum": total_sum
    }

