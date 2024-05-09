from flask import Blueprint, request, make_response
from ..models.models import Services
from .. import db
from ..services.plan import new_plan,edit_plan ,del_plan,get_plans,convert #,edit_service,del_service,upload_pic_service
plan_routes = Blueprint('plan_routes', __name__)

@plan_routes.route('/createplan', methods=['POST'])
def create_plan():
    data = request.json
    response, status_code = new_plan(data)
    return make_response(response, status_code)


@plan_routes.route('/updateplan',methods=['PUT'])
def update_plan() : 
    data = request.json 
    response, status_code = edit_plan(data)
    return make_response(response, status_code)


@plan_routes.route('/deleteplan/<int:plan_id>',methods=['DELETE'])
def delete_plan(plan_id): 
    response, status_code = del_plan(plan_id)
    return make_response(response, status_code)


@plan_routes.route('/getplans/<int:service_id>', methods=['GET'])
def get_plans_by_service(service_id) : 
    response, status_code = get_plans(service_id)
    return make_response(response, status_code)

@plan_routes.route('/convertmonaire/', methods=['POST'])
def convert_monaire() :
    data = request.json
    plan_id = data.get('plan_id') 
    to_currency = data.get('currency')
    
    response, status_code = convert(plan_id,to_currency)
    return make_response(response, status_code)