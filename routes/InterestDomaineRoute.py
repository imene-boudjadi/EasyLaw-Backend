from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
from ..services.domaine import new_domaine ,add_interest,get_interests
from ..services.services import token_required

interest_domaine_routes = Blueprint('interest_domaine_routes', __name__)

@interest_domaine_routes.route('/createdomaine', methods=['POST'])
def create_domaine():
    data = request.json
    response, status_code = new_domaine(data)
    return make_response(response, status_code)



@interest_domaine_routes.route('/addinterest', methods=['POST'])
@token_required
def create_interest(current_user):
    data = request.json
    response, status_code = add_interest(data,current_user)
    return make_response(response, status_code)

@interest_domaine_routes.route('/getmyinterest', methods=['GET'])
@token_required
def get_my_intersts(current_user):
    response, status_code = get_interests(current_user)
    return make_response(response, status_code)


