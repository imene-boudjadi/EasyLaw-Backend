from flask import Blueprint, request, make_response
from ..models.models import Services
from .. import db
from ..services.service import new_service,edit_service,del_service,upload_pic_service,get_services
service_routes = Blueprint('service_routes', __name__)

@service_routes.route('/createservice', methods=['POST'])
def create_service():

    if request.content_type == 'application/json':
        data = request.json
    else :
        data = {
            'description': request.form.get('description'),
            'nomService': request.form.get('nomService'),
        }
        if 'file' not in request.files:
            file = request.files['file']
            url = upload_pic_service(file)
            data['pic'] = url
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




@service_routes.route('/getAllServices', methods=['GET'])
def get_all_services() : 
    response, status_code = get_services()
    return make_response(response, status_code)


    

