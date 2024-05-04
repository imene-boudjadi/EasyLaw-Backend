# services.py

from ..models.models import *
from .. import db





def get_moderators():
    moderators=Acteur.query.filter_by(deleted=False,role="moderator").all()
    moderators_list=[]
    for moderator in moderators:
        
        
        moderator={
            'id': moderator.id,
            'userName': moderator.userName,
            'Email': moderator.Email,
            'role': moderator.role,
            'deleted': moderator.deleted,
            'infoContact': moderator.infoContact
        }
        moderators_list.append(moderator)  
    return moderators_list 





def getUsers(page=1, per_page=10):
    paginated_users = Acteur.query.filter_by(deleted=False, role="user").paginate(page=page, per_page=per_page, error_out=True, max_per_page=None)
    result = []
    for user in paginated_users.items:
        result.append({
            'id': user.id,
            'userName': user.userName,
            'Email': user.Email,
            'role': user.role,
            'deleted': user.deleted,
            'infoContact': user.infoContact
        })
    return result

def delete_user(id):
    
    
    if id:
        user_to_update = Acteur.query.get(id)
        if not user_to_update:
            return None  
        else:
         setattr(user_to_update, 'deleted', True)
         db.session.commit()
         return True



def add_new_moderator(data):
    new_moderator = Acteur(**data)
    db.session.add(new_moderator)
    db.session.flush()  # pour recuperer lid du moderateur ajouté 
    
    db.session.commit()
    return new_moderator


def update_moderator(data):
    
    moderator_id = data.pop('id', None)
    if moderator_id:
        moderator_to_update = Acteur.query.get(moderator_id)
        if not moderator_to_update:
            return None  
        for key, value in data.items():
            setattr(moderator_to_update, key, value)
    

    
            
    db.session.commit()
    return moderator_to_update


