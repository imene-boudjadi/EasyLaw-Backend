# services.py

from ..models.models import *
from .. import db

from flask import jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import request
from functools import wraps


import logging

# Créer un logger
logger = logging.getLogger(__name__)

# Définir le niveau de log
logger.setLevel(logging.INFO)

# Créer un gestionnaire de fichier
handler = logging.FileHandler('logfile.log')

# Créer un formateur et ajouter au gestionnaire
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Ajouter le gestionnaire au logger
logger.addHandler(handler)




def get_moderators():
    moderators=Users.query.filter_by(deleted=False,role="moderateur").all()
    moderators_list=[]
    for moderator in moderators:
        
        
        moderator={
            'id': moderator.id,
            'userName': moderator.username,
            'Email': moderator.email,
            'role': moderator.role,
            'deleted': moderator.deleted,
            'phoneNumber': moderator.phoneNumber
        }
        moderators_list.append(moderator)  
    
    logger.info(f'Retrieved {len(moderators_list)} moderators')
    
    return moderators_list





def getUsers(page=1, per_page=6):
    paginated_users = Users.query.filter_by(deleted=False, role="user").paginate(page=page, per_page=per_page, error_out=True, max_per_page=None)
    result = []
    for user in paginated_users.items:
        result.append({
            'id': user.id,
            'userName': user.username,
            'Email': user.email,
            'role': user.role,
            'deleted': user.deleted,
            'phoneNumber': user.phoneNumber
        })
        
    logger.info(f'Retrieved {len(result)} users on page {page} with {per_page} users per page')
        
    return result




def getModeratorById(id):
   user = Users.query.get(id)
   
   if user is None:
       return None

   result = {
            'id': user.id,
            'userName': user.username,
            'Email': user.email,
            'role': user.role,
            'deleted': user.deleted,
            'phoneNumber': user.phoneNumber
        }
    
   logger.info(f'moderator  with id {user} was sollicitated')

   return result


def delete_user(id):
    
    
    if id:
        user_to_update = Users.query.get(id)
        if not user_to_update:
            return None  
        else:
         setattr(user_to_update, 'deleted', True)
         db.session.commit()
         logger.info(f'Updated user with id {user_to_update}')

         return True



def add_new_moderator(data):
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password
    new_moderator = Users(**data)
    db.session.add(new_moderator)
    db.session.flush()  # pour recuperer lid du moderateur ajouté 
    

    logger.info(f'Added new moderator with id {new_moderator.id}')

    db.session.commit()
    return new_moderator

def update_moderator(data):
    
    moderator_id = data.pop('id', None)
    
    if moderator_id:
        moderator_to_update = Users.query.get(moderator_id)
        if not moderator_to_update:
            return None  
        for key, value in data.items():
            setattr(moderator_to_update, key, value)
        
        logger.info(f'Updated moderator with id {moderator_id}')
    
    db.session.commit()
    return moderator_to_update





