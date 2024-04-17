# route.py

from flask import Blueprint, request, make_response
from .services.services import signup, login, getAllFunds, createFund

routes = Blueprint('routes', __name__)

@routes.route("/signup", methods=["POST"])
def signup_route():
    return signup(request)

@routes.route("/login", methods=["POST"])
def login_route():
    return login(request)

@routes.route("/funds", methods=["GET"])
def get_all_funds_route():
    return getAllFunds(request)

@routes.route("/funds", methods=["POST"])
def create_fund_route():
    return createFund(request)
