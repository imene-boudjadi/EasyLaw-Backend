from .. import db
from flask import Blueprint, request, make_response
from ..models.models import Services
import os
from flask import jsonify

# i need to add upload photo and if it doesn't exist i add by default one 
def new_service(data): 
        nom_service = data.get('nomService')
        description = data.get('description')
        pic = data.get('pic')
        

        if(nom_service and description ) :
            if(pic is not None) : 
                new_service = Services(nomService=nom_service, description=description, pic=pic)
            else : 
                new_service = Services(nomService=nom_service, description=description, pic="")
        else : 
            return {'error': "nom_service and description are required "}, 400
        
        try:
            db.session.add(new_service)
            db.session.commit()
            return {'message': 'Service created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        



def edit_service(data): 
    service_id = data.get('service_id')
    if(service_id is None) : 
        return {'error': 'service_id is required '}, 404

    service = Services.query.get(service_id)
    if not service:
        return {'error': 'Service not found'}, 404

    if 'nomService' in data:
        service.nomService = data['nomService']
    if 'description' in data:
        service.description = data['description']
    if 'pic' in data:
        service.pic = data['pic']

    try:
        db.session.commit()
        return {'message': 'Service updated successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
    

def del_service(service_id):

    if(service_id is None) : 
        return {'error': 'service_id is required '}, 404
    service = Services.query.get(service_id)
    if not service:
        return {'error': 'Service not found'}, 404

    try:
        db.session.delete(service)
        db.session.commit()
        return {'message': 'Service deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

     


def get_services() : 
    try:
        services = Services.query.all()
        serialized_services = [service.serialize for service in services]
        return jsonify({"data" :serialized_services}), 200
    except Exception as e:
        # Return an error response if there's an exception
        return jsonify({'error': str(e)}), 500
