from flask import Blueprint, request, make_response
from ..models.models import Services
from .. import db
from ..services.service import new_service,edit_service,del_service,upload_pic_service
service_routes = Blueprint('service_routes', __name__)

@service_routes.route('/createservice', methods=['POST'])
def create_service():
    data = request.json
    response, status_code = new_service(data)
    return make_response(response, status_code)


@service_routes.route('/updateservice',methods=['PUT'])
def update_service() : 
    data = request.json 
    response, status_code = edit_service(data)
    return make_response(response, status_code)


@service_routes.route('/deleteservice/<int:service_id>',methods=['DELETE'])
def delete_service(service_id): 
    response, status_code = del_service(service_id)
    return make_response(response, status_code)


@service_routes.route('/uploadservicephoto', methods=['POST'])
def upload_pic():
    if 'file' not in request.files:
       return make_response({"error":"No image uploaded"},400 )
    
    file = request.files['file']
    response, status_code = upload_pic_service(file)
    return make_response(response, status_code)


    

