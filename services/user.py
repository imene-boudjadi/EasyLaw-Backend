# services.py

from flask import request
from ..models.user import Users, Funds , RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from .. import db



def signup(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    phoneNumber = data.get("phoneNumber")

    if username and email and password and role:
        user = Users.query.filter_by(email=email).first()
        if user:
            return {"message": "Please sign in"}, 200
        user = Users(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=RoleEnum(role),
            phoneNumber=phoneNumber
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

def update_user_info(data, current_user):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phoneNumber = data.get("phoneNumber")
    secondPhoneNumber = data.get("secondPhoneNumber")  
    address = data.get("address")                      

    if not (username or email or password or phoneNumber or secondPhoneNumber or address): # aucun champs n est modifié
        return {"message": "No fields to update"}, 400

    if username and username != current_user.username: # Mise à jour des infos
        current_user.username = username
    if email and email != current_user.email:
        current_user.email = email
    if password and password != current_user.password:
        current_user.password = generate_password_hash(password)
    if phoneNumber and phoneNumber != current_user.phoneNumber:
        current_user.phoneNumber = phoneNumber
    if secondPhoneNumber and secondPhoneNumber != current_user.secondPhoneNumber:  # Mise à jour du second numéro de téléphone
        current_user.secondPhoneNumber = secondPhoneNumber
    if address and address != current_user.address:  # Mise à jour de l'adresse
        current_user.address = address

    db.session.commit()
    return {"message": "User information updated successfully"}




