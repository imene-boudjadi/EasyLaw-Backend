from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
moderator_routes = Blueprint('moderator_routes', __name__)

from flask import jsonify
from ..services.adminService import *

#http://localhost:5000/users_with_subscriptions?page=1&per_page=20
@moderator_routes.route('/users_with_subscriptions', methods=['GET'])
def get_users_subscriptions():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = get_users_with_subscriptions(page=page, per_page=per_page)
    return jsonify(users)
    
@moderator_routes.route('/moderators',methods=['GET'])
def get_moderators():
    moderators=getAdminsWithContactInfos()
    return jsonify(moderators)

@moderator_routes.route('/add_moderator',methods=['POST'])
def add_moderator():
    data = request.get_json()
    new_moderator=add_new_moderator(data)
    return jsonify(new_moderator.to_dict()), 201

@moderator_routes.route('/update_moderator', methods=['POST'])
#http://localhost:5000/add_update_moderator?page=1&per_page=20

def add_update_moderator_route():
    data = request.get_json()
    moderator = add_update_moderator(data)
    if moderator is None:
        return jsonify({'error': 'Moderator not found'}), 404
    return jsonify(moderator.to_dict()), 201

@moderator_routes.route('/delete_moderator', methods=['POST'])
#http://localhost:5000/delete_moderator?id=1

def delete_moderator_route():
    id= request.args.get('id',None,type=int)
    result=delete_moderator(id)
    if(result!=None):
         return  jsonify({'success': 'Moderator found'}),201
    else:
        return jsonify({'error': 'Moderator not found'}), 404


@moderator_routes.route('/bloc_moderator', methods=['POST'])
#http://localhost:5000/bloc_moderator?id=1

def bloc_moderator_route():
    id= request.args.get('id',None,type=int)
    result=bloc_moderator(id)
    if(result!=None):
         return  jsonify({'success': 'Moderator found'}),201
    else:
        return jsonify({'error': 'Moderator not found'}), 404

@moderator_routes.route('/unbloc_moderator', methods=['POST'])
#http://localhost:5000/unbloc_moderator?id=1

def unbloc_moderator_route():
    id= request.args.get('id',None,type=int)
    result=unbloc_moderator(id)
    if(result!=None):
         return  jsonify({'success': 'Moderator found'}),201
    else:
        return jsonify({'error': 'Moderator not found'}), 404

@moderator_routes.route('/delete_user', methods=['POST'])
#http://localhost:5000/delete_user?id=1

def delete_user_route():
    id= request.args.get('id',None,type=int)
    result=delete_user(id)
    if(result!=None):
         return jsonify({'error': 'user  found'}), 201
    else:
        return jsonify({'error': 'Moderator not found'}), 404
    
@moderator_routes.route('/bloc_user', methods=['POST'])
#http://localhost:5000/bloc_user?id=1

def bloc_user_route():
    id= request.args.get('id',None,type=int)
    result=bloc_user(id)
    if(result!=None):
         return  jsonify({'success': 'Moderator found'}),201
    else:
        return jsonify({'error': 'user not found'}), 404

@moderator_routes.route('/unbloc_user', methods=['POST'])
#http://localhost:5000/unbloc_user?id=1

def unbloc_user_route():
    id= request.args.get('id',None,type=int)
    result=unbloc_user(id)
    if(result!=None):
         return  jsonify({'error': 'user  found'}),201
    else:
        return jsonify({'error': 'user not found'}), 404

