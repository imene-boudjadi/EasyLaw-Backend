from flask import Blueprint, request, make_response, redirect
from ..services.subscribtion import subscribe, handleWebhook, get_subscriptions_by_user, get_invoices_by_user
from flask import jsonify
import jwt

subscribtion_routes = Blueprint('subscribtion_routes', __name__)

@subscribtion_routes.route("/subscribe", methods=["POST"])
def subscribe_route():
    data = request.json
    response, status_code = subscribe(data)
    return make_response(response, status_code)


@subscribtion_routes.route("/subscribtions/<int:user_id>", methods=["GET"])
def get_subscribtions_route(user_id):
    response, status_code = get_subscriptions_by_user(user_id)
    return make_response(response, status_code)


@subscribtion_routes.route("/invoices/<int:user_id>", methods=["GET"])
def get_invoices_route(user_id):
    response, status_code = get_subscriptions_by_user(user_id)
    return make_response(response, status_code)


@subscribtion_routes.route('/webhook/', methods=['POST'])
def webhook():
    response, status_code = handleWebhook(request)
    return make_response({"message": response}, status_code)



