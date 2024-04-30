from flask import Blueprint, request, make_response
from ..models.models import Services
from .. import db
from ..services.plan import new_plan,edit_plan #,edit_service,del_service,upload_pic_service
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

