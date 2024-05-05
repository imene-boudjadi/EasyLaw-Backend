from ..models.models import *
from .. import db

from flask import jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import request
from functools import wraps


def update_moderator(data):
    
    moderator_id = data.pop('id', None)
    if moderator_id:
        moderator_to_update = Users.query.get(moderator_id)
        if not moderator_to_update:
            return None  
        for key, value in data.items():
            setattr(moderator_to_update, key, value)
    

    
            
    db.session.commit()
    return moderator_to_update


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