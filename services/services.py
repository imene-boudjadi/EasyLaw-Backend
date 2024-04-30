# services.py

from ..models.models import Payement, Acteur,infoContact,AbonnementService,Service
from .. import db








def getUsers(page=1, per_page=10):
    paginated_users=Acteur.query.filter_by(deleted=False ).filter_by(role="user").paginate(page=page, per_page=per_page, error_out=True, max_per_page=None)    
    result=[]
    for user in paginated_users:
        contacts_user=[]
        contacts=[]
        infos_payement=[]
        contacts=infoContact.query.filter_by(acteur=user.id).all()
        payements= Payement.query.filter_by(acteur_id=user.id).all()
        


        for payement in payements:
            if payement:
                abonnement = AbonnementService.query.get(payement.abonnement_id)
                service = Service.query.get(abonnement.service_id)
                infos_payement.append({
                    'nom' :abonnement.nom,
                    'duree' : abonnement.duree,
                    'description' : abonnement.description,
                    'date_paiement':payement.date_paiement,
                    'service':service.nom
        
                })


        for conntact in user.contacts:
            if conntact:
                contacts_user.append({'id':conntact.id,
                        'designation':conntact.designation,
                        'value':conntact.value
                    })
        
        result.append({
            'id':user.id,
            'userName ':user.userName,
    

      
        
             'Email ':user.Email,
             'infos_contact':contacts_user,
             'abonnements':infos_payement

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

def get_moderators():
    moderators=Acteur.query.filter_by(role="moderator").all()
    moderators_list=[]
    for moderator in moderators:
        contacts_moderator=[]
        for conntact in moderator.contacts:
            if conntact:
                contacts_moderator.append({'id':conntact.id,
                        'designation':conntact.designation,
                        'value':conntact.value
                    })
        moderator={
                'id':moderator.id,
                'userName ':moderator.userName,
                'deleted':moderator.deleted,

      
        
             'Email ':moderator.Email,
             'infos_contact':contacts_moderator,
        }
        moderators_list.append(moderator)  
    return moderators_list     

    
def delete_moderator(id):
    
    
    if id:
        moderator_to_update = Acteur.query.get(id)
        if not moderator_to_update:
            return None  
        else:
         setattr(moderator_to_update, 'deleted', True)
         db.session.commit()
         return True


def add_new_moderator(data):
    contacts_data = data.pop('infos_Contact', [])
    new_moderator = Acteur(**data)
    db.session.add(new_moderator)
    db.session.flush()  # pour recuperer lid du moderateur ajouté 
    for contact_data in contacts_data:
        new_contact = infoContact(acteur=new_moderator.id, **contact_data)
        db.session.add(new_contact)
    db.session.commit()
    return new_moderator





 

def update_moderator(data):
    contacts_data = data.pop('infos_Contact', [])
    moderator_id = data.pop('id', None)
    if moderator_id:
        moderator_to_update = Acteur.query.get(moderator_id)
        if not moderator_to_update:
            return None  
        for key, value in data.items():
            setattr(moderator_to_update, key, value)
    else:
        moderator_to_update = Acteur(**data)
        db.session.add(moderator_to_update)
        db.session.flush()  

    for contact_data in contacts_data:
        contact_id = contact_data.pop('id', None)
        if contact_id:
            # Récupérer le contact existant
            contact_to_update = infoContact.query.get(contact_id)
            if not contact_to_update:
                return None
            # Mettre à jour les valeurs du contact
            for key, value in contact_data.items():
                setattr(contact_to_update, key, value)
        else:
            # Créer un nouveau contact si aucun id n'est fourni
            new_contact = infoContact(acteur=moderator_to_update.id, **contact_data)
            db.session.add(new_contact)
    db.session.commit()
    return moderator_to_update


























  
"""def get_users_with_subscriptions(page=1, per_page=10):
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
         """
















"""
def signup(data):
    firstName = data.get("firstName")
    LastName = data.get("LastName")
    email = data.get("email")
    password = data.get("password")

    if firstName and LastName and email and password:
        user = Users.query.filter_by(email=email).first()
        if user:
            return {"message": "Please sign in"}, 200
        user = Users(
            email=email,
            password=generate_password_hash(password),
            firstName=firstName,
            LastName=LastName
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User Created"}, 201
    return {"message": "Unable to create user"}, 500

def login(auth):
    if not auth or not auth.get("password"):
        return "Proper Credentials were not provided", 401
    user = Users.query.filter_by(email=auth.get("email")).first()
    if not user:
        return "Please create an account", 401
    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
            "secret",
            "HS256"
        )
        return jsonify({'token': token}), 201
    return "Please check your credentials", 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {"message": "Token is missing"}, 401
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
            print(current_user)
        except Exception as e:
            print(e)
            return {"message": "Token is invalid"}, 401
        return f(current_user, *args, **kwargs)
    return decorated

def get_all_funds(current_user):
    funds = Funds.query.filter_by(userId=current_user.id).all()
    total_sum = 0

    if funds:
        total_sum = db.session.query(func.round(func.sum(Funds.amount), 2)).filter_by(userId=current_user.id).scalar()

    serialized_funds = [{"id": fund.id, "amount": fund.amount} for fund in funds]

    return {
        "data": serialized_funds,
        "sum": total_sum
    }

def create_fund(data, current_user):
    amount = data.get("amount")
    if amount:
        fund = Funds(
            amount=amount,
            userId=current_user.id
        )
        db.session.add(fund)
        db.session.commit()
    return {"message": "Fund created successfully"}



"""