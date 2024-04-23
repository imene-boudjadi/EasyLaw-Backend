# services.py

from flask import request
from ..models.models import Users, Funds
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from .. import db




def signup(data):
    firstName = data.get("firstName")
    LastName = data.get("LastName")
    email = data.get("email")
    password = data.get("password")

    if firstName and LastName and email and password:
        user = Users.query.filter_by(email=email).first()
        if user:
            return {"message": "Please sign in"}, 200
        user = Users(
            email=email,
            password=generate_password_hash(password),
            firstName=firstName,
            LastName=LastName
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User Created"}, 201
    return {"message": "Unable to create user"}, 500

def login(auth):
   
    if not auth or not auth.get("password"):
        return "Proper Credentials were not provided", 401
    user = Users.query.filter_by(email=auth.get("email")).first()
    if not user:
        return "Please create an account", 401
    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
            "secret",
            "HS256"
        )
        return jsonify({'token': token}), 201
    return "Please check your credentials", 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {"message": "Token is missing"}, 401
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
            print(current_user)
        except Exception as e:
            print(e)
            return {"message": "Token is invalid"}, 401
        return f(current_user, *args, **kwargs)
    return decorated

def get_all_funds(current_user):
    funds = Funds.query.filter_by(userId=current_user.id).all()
    total_sum = 0

    if funds:
        total_sum = db.session.query(func.round(func.sum(Funds.amount), 2)).filter_by(userId=current_user.id).scalar()

    serialized_funds = [{"id": fund.id, "amount": fund.amount} for fund in funds]

    return {
        "data": serialized_funds,
        "sum": total_sum
    }

def create_fund(data, current_user):
    amount = data.get("amount")
    if amount:
        fund = Funds(
            amount=amount,
            userId=current_user.id
        )
        db.session.add(fund)
        db.session.commit()
    return {"message": "Fund created successfully"}



