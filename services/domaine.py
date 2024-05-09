from flask import request
from ..models.models import  InterestDomaines,ActeurDomaines
from flask import jsonify
# import jwt
# from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from .. import db



def new_domaine(data):
   
    nom = data.get('nom')
    if( nom ) :
        new_domaine = InterestDomaines(nom=nom) 
    else : 
        return {'error': "nom is required "}, 400

    try:
        db.session.add(new_domaine)
        db.session.commit()
        return {'message': 'Domaine created successfully'}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
    

def add_interest(data,current_user):
    acteur_id=current_user.id
    domaine_id=data.get('interestDomaine_id')

    if(domaine_id is None):
        return {'error': 'interestDomaine_id is required  '}, 404

    domaine = InterestDomaines.query.get(domaine_id)
    if not domaine:
            return {'error': 'No Domaine with this id '}, 404
    if(domaine_id) :
        new_interest= ActeurDomaines(acteur_id=acteur_id,interet_id=domaine_id)
    else :
        return {'error': "interestDomaine_id is required "}, 400

    try:
        db.session.add(new_interest)
        db.session.commit()
        return {'message': 'Interest created successfully'}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

def get_interests(current_user):
    try:
       
        acteur_domaine = ActeurDomaines.query.filter_by(acteur_id=current_user.id).all()

        # Extract the interest IDs from the ActeurDomaines
        interest_ids = [ad.interet_id for ad in acteur_domaine]

        # Query InterestDomaines using the extracted IDs
        interests = InterestDomaines.query.filter(InterestDomaines.id.in_(interest_ids)).all()

        # Serialize the interests
        serialized_interests = [{
            "id": interest.id,
            "nom": interest.nom
        } for interest in interests]

        # Return the serialized interests
        return jsonify(serialized_interests), 200
                   
      
    
    except Exception as e:
        # Return an error response if there's an exception
        return jsonify({'error': str(e)}), 500