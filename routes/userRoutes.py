from flask import Blueprint, request, make_response
from ..services.user import  login, token_required


user_routes = Blueprint('user_routes', __name__)



@user_routes.route("/login", methods=["POST"])
def login_route():
    auth = request.json
    response, status_code = login(auth)
    return make_response(response, status_code)