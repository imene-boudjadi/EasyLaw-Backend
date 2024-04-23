from ..models.adminModels import User, Abonnement_user,AbonnementService,admins,infos_Contact
from .. import db

def get_users_with_subscriptions(page=1, per_page=10):
    paginated_users = User.query.filter_by(deleted=False).paginate(page=page, per_page=per_page, error_out=True, max_per_page=None)
    result = []

    for user in paginated_users.items:
        subscriptions_user = Abonnement_user.query.filter_by(user_id=user.id).all()
        user_subscriptions = []
        for subscription_user in subscriptions_user:
            subscription = AbonnementService.query.filter_by(id=subscription_user.abonnement_id).first()
            if subscription:
                user_subscriptions.append({
                    'planTarification': subscription.planTarification,
                    'status': subscription.status,
                    'Service': subscription.Service,
                    'date_debut': subscription_user.Date_debut,
                    'date_fin': subscription_user.date_fin
                })

        user_data = {
            'id': user.id,
            'userName': user.userName,
            'Email': user.Email,
            'phone_number': user.phone_number,
            'subscriptions': user_subscriptions,
            'state': user.bloqued,
            'deleted':user.deleted
        }
        result.append(user_data)

    return result

def getAdminsWithContactInfos():
    admins_list=admins.query.filter_by(deleted=False).all()
    result=[]
    
    
    for admin in admins_list:
        contacts_admin=[]
        contacts_admin=infos_Contact.query.filter_by(admin=admin.id).all()
        
        contacts=[]
        for conntact in contacts_admin:
            if conntact:
                contacts.append({'id':conntact.id,
                        'designation':conntact.designation,
                        'value':conntact.value
                    })
                        
                
        result.append({
         

            'id': admin.id,
            'adminName': admin.adminName,
            'level': admin.level,

            'Email': admin.Email,
            'bloqued': admin.bloqued,
            'deleted':admin.deleted,
            'infos_Contact': contacts,
            
        })        
    return result






def add_new_moderator(data):
    contacts_data = data.pop('infos_Contact', [])
    new_moderator = admins(**data)
    db.session.add(new_moderator)
    db.session.flush()  # pour recuperer lid du moderateur ajouté 
    for contact_data in contacts_data:
        new_contact = infos_Contact(admin=new_moderator.id, **contact_data)
        db.session.add(new_contact)
    db.session.commit()
    return new_moderator

def add_update_moderator(data):
    contacts_data = data.pop('infos_Contact', [])
    moderator_id = data.pop('id', None)
    if moderator_id:
        moderator_to_update = admins.query.get(moderator_id)
        if not moderator_to_update:
            return None  
        for key, value in data.items():
            setattr(moderator_to_update, key, value)
    else:
       
        moderator_to_update = admins(**data)
        db.session.add(moderator_to_update)
        db.session.flush()  # This is needed to generate the id for the new moderator

    for contact_data in contacts_data:
        new_contact = infos_Contact(admin=moderator_to_update.id, **contact_data)
        db.session.add(new_contact)
    db.session.commit()
    return moderator_to_update


def delete_moderator(id):
    
    
    if id:
        moderator_to_update = admins.query.get(id)
        if not moderator_to_update:
            return None  
        else:
         setattr(moderator_to_update, 'deleted', True)
         db.session.commit()
         return True
         
def bloc_moderator(id):
    
    
    if id:
        moderator_to_update = admins.query.get(id)
        if not moderator_to_update:
            return None  
        else:
         setattr(moderator_to_update, 'bloqued', True)
         db.session.commit()
         return True

def unbloc_moderator(id):
    
    
    if id:
        moderator_to_update = admins.query.get(id)
        if not moderator_to_update:
            return None  
        else:
         setattr(moderator_to_update, 'bloqued', False)
         db.session.commit()
         return True
                            
       
def bloc_user(id):
    
    
    if id:
        user_to_update = User.query.get(id)
        if not user_to_update:
            return None  
        else:
         setattr(user_to_update, 'bloqued', True)
         db.session.commit()
         return True

def unbloc_user(id):
    
    
    if id:
        user_to_update = admins.query.get(id)
        if not user_to_update:
            return None  
        else:
         setattr(user_to_update, 'bloqued', False)
         db.session.commit()
         return True

def delete_user(id):
    
    
    if id:
        user_to_update = User.query.get(id)
        if not user_to_update:
            return None  
        else:
         setattr(user_to_update, 'deleted', True)
         db.session.commit()
         return True        