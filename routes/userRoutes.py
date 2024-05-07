from flask import Blueprint, request, make_response
from ..services.user import signup, login, token_required, get_all_funds, create_fund, update_user_info


user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/signup", methods=["POST"])
def signup_route():
    data = request.json
    response, status_code = signup(data)
    return make_response(response, status_code)

@user_routes.route("/login", methods=["POST"])
def login_route():
    auth = request.json
    response, status_code = login(auth)
    return make_response(response, status_code)

@user_routes.route("/funds", methods=["GET"])
@token_required
def get_all_funds_route(current_user):
    response_data = get_all_funds(current_user)
    return make_response(response_data)

@user_routes.route("/funds", methods=["POST"])
@token_required
def create_fund_route(current_user):
    data = request.json
    response_data = create_fund(data, current_user)
    return make_response(response_data)


@user_routes.route("/update-info", methods=["PUT"])
@token_required
def update_user_info_route(current_user):
    data = request.json
    response_data = update_user_info(data, current_user)
    return make_response(response_data)