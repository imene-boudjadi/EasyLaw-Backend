from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
moderator_routes = Blueprint('moderator_routes', __name__)
from flask_jwt_extended import decode_token
from flask import jsonify
from ..services.services import *
from flask import jsonify, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
          bearer, token = request.headers["Authorization"].split()
        if not token:
            return {"message": "Token is missing"}, 401
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
            if current_user.role != RoleEnum.admin:
                return {"message": "Admin access required"}, 403
        except Exception as e:
            print(e)
            return {"message": "Token is invalid"}, 401
        return f(current_user, *args, **kwargs)
    return decorated



@moderator_routes.route('/users', methods=['GET'])
@admin_required

#http://localhost:5000/users?page=1&per_page=20

def get_users_subscriptions_route(current_user):

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = getUsers(page=page, per_page=per_page)
    return jsonify(users)


@moderator_routes.route('/moderators',methods=['GET'])
@admin_required
#http://localhost:5000/moderator
def getmoderators_route(current_user):
    moderators=get_moderators()
    return jsonify(moderators)






@moderator_routes.route('/delete_user', methods=['POST'])
@admin_required

#http://localhost:5000/delete_user?id=1
def delete_user_route(current_user):
    id= request.args.get('id',None,type=int)
    result=delete_user(id)
    if(result!=None):
         return  jsonify({'success': 'user found'}),201
    else:
        return jsonify({'error': 'user not found'}), 404





@moderator_routes.route('/add_moderator', methods=['POST'])
@admin_required

def add_moderator_route(current_user):
    data = request.get_json()
    moderator = add_new_moderator(data)
    if moderator is None:
        return jsonify({'error': 'Moderator not found'}), 404
    return jsonify(moderator.to_dict()), 201





@moderator_routes.route('/update_moderator', methods=['POST'])
@admin_required

#http://localhost:5000/update_moderator?id=1

def update_moderator_route(current_user):
    data = request.get_json()
    moderator = update_moderator(data)
    if moderator is None:
        return jsonify({'error': 'Moderator not found'}), 404
    return jsonify(moderator.to_dict()), 201








