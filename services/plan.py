from .. import db
from flask import Blueprint, request, make_response
from ..models.models import PlanTarifications ,Services
import os


def new_plan(data): 
        service_id =data.get('service_id')  # Foreign key reference
        if(service_id is None):
            return {'error': 'service_id is required  '}, 404

        service = Services.query.get(service_id)
        if not service:
            return {'error': 'No service with this id '}, 404
        nom = data.get('nom')
        tarif = data.get('tarif')
        type_tarification =  data.get('type_tarification')
        # monnaire =  data.get('monnaire')
        durree =  data.get('durree')


        if(service_id and nom and tarif and type_tarification  and durree ) :
            if(type_tarification != "مخصص" and type_tarification != "مميز") :
                return {"error":"Unallowed type of tarification the allowed values are (مخصص or مميز)"},400
            elif (durree != 30 and durree != 365):
                return {"error":"Unallowed durree  (the allowed values are : 30 or 365)"},400
            else :
                new_plan = PlanTarifications(service_id=service_id,nom=nom,tarif=tarif ,monnaire="DZD" ,type_tarification=type_tarification,durree=durree) 
        else : 
            return {'error': "service_id , nom , tarif , type_tarification , durree are required "}, 400
        
        try:
            db.session.add(new_plan)
            db.session.commit()
            return {'message': 'Plan created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
 
