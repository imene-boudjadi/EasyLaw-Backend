from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
moderator_routes = Blueprint('moderator_routes', __name__)

from flask import jsonify
from ..services.services import *
from flask import jsonify, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps


@moderator_routes.route('/users', methods=['GET'])
#@admin_required

#http://localhost:5000/users?page=1&per_page=20

def get_users_subscriptions_route():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = getUsers(page=page, per_page=per_page)
    return jsonify(users)

#@admin_required
@moderator_routes.route('/moderators',methods=['GET'])
def getmoderators_route():
    moderators=get_moderators()
    return jsonify(moderators)

@moderator_routes.route('/delete_user', methods=['POST'])
#@admin_required

#http://localhost:5000/delete_user?id=1
def delete_user_route():
    id= request.args.get('id',None,type=int)
    result=delete_user(id)
    if(result!=None):
         return  jsonify({'success': 'user found'}),201
    else:
        return jsonify({'error': 'user not found'}), 404



@moderator_routes.route('/add_moderator', methods=['POST'])
#@admin_required

def add_moderator_route():
    data = request.get_json()
    moderator = add_new_moderator(data)
    if moderator is None:
        return jsonify({'error': 'Moderator not found'}), 404
    return jsonify(moderator.to_dict()), 201


@moderator_routes.route('/update_moderator', methods=['POST'])
#@admin_required

#http://localhost:5000/update_moderator?id=1

def update_moderator_route():
    data = request.get_json()
    moderator = update_moderator(data)
    if moderator is None:
        return jsonify({'error': 'Moderator not found'}), 404
    return jsonify(moderator.to_dict()), 201






"""
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = getUserByid(current_user_id)
        if current_user.role != 'admin':
            return jsonify(error="User is not an admin"), 403
        return fn(*args, **kwargs)
    return wrapper
"""


"""
























#moderator_routes:

@moderator_routes.route('/auto_web_scrapping_sources', methods=['POST'])
def get_auto_web_scrapping_sources_route():

    sources=getWebScrappingSources()
    return jsonify(sources)





"""










"""@moderator_routes.route('/protected', methods=['GET'])


def protected():
    try:
        # Essayer de décoder le token
        current_user_id = get_jwt_identity()
    except:
        # Si le token est corrompu, renvoyer une erreur
        return jsonify(error="Invalid token"), 400

    if current_user_id is None:
        # Si l'utilisateur n'est pas connecté, redirigez-le vers la page d'inscription
        return jsonify({'error': 'redirection'}),300
        #return redirect(url_for('signup'))

    # Récupérez l'utilisateur de la base de données
    current_user = getUserByid(current_user_id)
    if current_user is None:
        return jsonify(error="User not found"), 404

    if current_user.role != 'admin':
        # Si l'utilisateur n'est pas un administrateur, renvoyez une erreur
        return jsonify(error="User is not an admin"), 403

    # L'utilisateur est connecté et est un administrateur
    # Ici, vous pouvez exécuter vos fonctions protégées
    # ...
    return jsonify(success=True), 200




"""
