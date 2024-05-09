from .. import db
from flask import Blueprint, request, make_response
from ..models.models import PlanTarifications ,Services
import os
from flask import jsonify
from forex_python.converter import CurrencyRates



def new_plan(data): 
        service_id =data.get('service_id')  
        if(service_id is None):
            return {'error': 'service_id is required  '}, 404

        service = Services.query.get(service_id)
        if not service:
            return {'error': 'No service with this id '}, 404
        nom = data.get('nom')
        tarif = data.get('tarif')
        type_tarification =  data.get('type_tarification')


        if(service_id and nom and tarif and type_tarification   ) :
            new_plan = PlanTarifications(service_id=service_id,nom=nom,tarif=tarif ,monnaire="DZD" ,type_tarification=type_tarification) 
        else : 
            return {'error': "service_id , nom , tarif , type_tarification"}, 400
        
        try:
            db.session.add(new_plan)
            db.session.commit()
            return {'message': 'Plan created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
 

def edit_plan(data) : 
    
    plan_id = data.get('plan_id')
    if(plan_id is None) : 
        return {'error': 'plan_id is required '}, 404

    plan = PlanTarifications.query.get(plan_id)
    if not plan:
        return {'error': 'Plan not found'}, 404

    if 'nom' in data:
        plan.nom = data['nom']
    if 'tarif' in data:
        plan.tarif = data['tarif']
    if 'type_tarification' in data:
        if(data['type_tarification'] != "مخصص" and data['type_tarification'] != "مميز") :
                return {"error":"Unallowed type of tarification the allowed values are (مخصص or مميز)"},400
        plan.type_tarification = data['type_tarification']

    if 'durree' in data:
        if(data['durree'] != 30 and data['durree'] != 365) : 
            return {"error":"Unallowed durree  (the allowed values are : 30 or 365)"},400
        plan.durree = data['durree']

    try:
        db.session.commit()
        return {'message': 'Plan updated successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
    


def del_plan(plan_id) :
    if(plan_id is None) : 
        return {'error': 'plan_id is required '}, 404
    plan = PlanTarifications.query.get(plan_id)
    if not plan:
        return {'error': 'Plan not found'}, 404

    try:
        db.session.delete(plan)
        db.session.commit()
        return {'message': 'Plan deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
    

def get_plans(service_id) : 
    try:
        if(service_id is None) : 
            return {'error': 'service_id is required '}, 404
        service = Services.query.get(service_id)
        if not service:
            return {'error': 'No Service with this Id'}, 404 
                   
        plans = PlanTarifications.query.filter_by(service_id=service_id).all()
        serialized_plans = [plan.serialize for plan in plans]
        return jsonify({"data" : serialized_plans }), 200
    
    except Exception as e:
        # Return an error response if there's an exception
        return jsonify({'error': str(e)}), 500


def convert_currency(price, from_currency, to_currency):
    import requests

    import requests

    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
    querystring = {"from":from_currency,"to":to_currency,"amount":price}
    headers = {
        "X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
        "X-RapidAPI-Host": os.getenv("X-RapidAPI-Host")
    }

    response = requests.get(url, headers=headers, params=querystring)
    json_response = response.json()
    if(json_response['success']) :
        return response.json()['result']
    else :
        return -1



def convert(plan_id ,to_currency ) : 
    try:

        if(plan_id is None) : 
            return {'error': 'plan_id is required '}, 404
        plan = PlanTarifications.query.get(plan_id)
        if not plan:
            return {'error': 'Plan not found'}, 404
       
        new_tarif = convert_currency(plan.tarif,"DZD",to_currency)
        if(new_tarif ==-1 ) : 
            return jsonify({'error': 'Invalid currency'}), 404

        if plan:
            serialized_plan = plan.serialize
            serialized_plan['new_tarif'] = new_tarif
            return jsonify(serialized_plan), 200
        else:
            # Return a 404 error response if the plan is not found
            return jsonify({'error': 'Plan tariff not found'}), 404
    except Exception as e:
        # Return an error response if there's an exception
        return jsonify({'error': str(e)}), 500