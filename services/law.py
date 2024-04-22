
from flask import request
from ..models.models import  Law
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

def get_all_unique_wizara():
    unique_wizara = Law.query.with_entities(Law.wizara).distinct().all()
    unique_wizara = [w[0] for w in unique_wizara]  # Extracting wizara values from tuples

    return unique_wizara

def get_all_laws_with_sum():
    laws = Law.query.all()

    total_sum = db.session.query(func.sum(Law.idLaw)).scalar()

    return {
        "data": laws,
        "sum": total_sum
    }

