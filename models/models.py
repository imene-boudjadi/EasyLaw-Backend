from .. import db
from sqlalchemy import func
from datetime import datetime

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    role = db.Column(db.String(255), nullable=False)
    deleted= db.Column(db.Boolean, nullable=False)
    acteur_domaine = db.relationship('ActeurDomaines', backref='users')
    payement = db.relationship('Payements', backref='users', lazy=True, cascade='all, delete-orphan')
    token = db.relationship('AccessTokens', backref='users', lazy=True, cascade='all, delete-orphan')
    customer_id = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<User {self.firstName} {self.id}>'


class Funds(db.Model):
    __tablename__ = "Funds"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2))
    userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user = db.relationship("Users", backref="funds")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "created_at": self.created_at
        }

class Law(db.Model):
    __tablename__ = "law"

    idLaw = db.Column(db.Integer, primary_key=True)
    wizara = db.Column(db.String(255))
    sujet = db.Column(db.Text)
    type = db.Column(db.String(255))
    num = db.Column(db.String(255))
    date = db.Column(db.String(255))
    num_jarida = db.Column(db.Integer)
    date_jarida = db.Column(db.String(255))
    page_jarida = db.Column(db.Integer)
    def __repr__(self):
        return f'<Law {self.idLaw}>'
    


class Services(db.Model):
    __tablename__ = "Services"
    id = db.Column(db.Integer, primary_key=True)
    nomService = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pic = db.Column(db.String(255), nullable=False)
    plan = db.relationship('PlanTarifications', backref='service', lazy=True, cascade='all, delete-orphan')
    token = db.relationship('AccessTokens', backref='service', lazy=True, cascade='all, delete-orphan')
    abonement = db.relationship('AbonementServices', backref='service', lazy=True, cascade='all, delete-orphan')


    @property
    def serialize(self):
        return {
            "id": self.id,
            "nomService": self.nomService,
            "description": self.description
        }
    
    def __repr__(self):
        return f'<Service {self.id}>'

class Payements(db.Model) : 
    __tablename__ = "Payements"
    id = db.Column(db.Integer, primary_key=True)
    abonement_id  = db.Column(db.Integer, db.ForeignKey('AbonementServices.id')) 
    acteur_id = db.Column(db.Integer, db.ForeignKey('Users.id')) 
    date_paiement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    moyen_payment = db.Column(db.String(255), nullable=False)

class AbonementServices(db.Model):
    __tablename__ = "AbonementServices"
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('PlanTarifications.id'))  # Foreign key reference
    payement = db.relationship('Payements', backref='abonement', lazy=True, cascade='all, delete-orphan')
    access_token_id = db.Column(db.Integer, db.ForeignKey('AccessTokens.id')) 
    service_id =  db.Column(db.Integer, db.ForeignKey('Services.id'))  
    date_abonement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    checkout_id = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<AbonementService {self.id}>'

class AccessTokens(db.Model) : 
    __tablename__="AccessTokens"
    id = db.Column(db.Integer, primary_key=True)
    acteur_id = db.Column(db.Integer, db.ForeignKey('Users.id'))  
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'))  
    expires = db.Column(db.DateTime, nullable=False)
    abonement = db.relationship('AbonementServices', backref='accessTokens', lazy=True, cascade='all, delete-orphan')



class PlanTarifications(db.Model):
    __tablename__="PlanTarifications"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'))  
    nom = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    tarif = db.Column(db.Float, nullable=False)
    type_tarification = db.Column(db.String(255), nullable=False)
    monnaire = db.Column(db.String(255), nullable=False)
    durree = db.Column(db.Integer, nullable=False)
    abonement = db.relationship('AbonementServices', backref='plan', lazy=True, cascade='all, delete-orphan')
    price_id = db.Column(db.String(255), nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "tarif": self.tarif,
            "type_tarification": self.type_tarification,
            "monnaire": self.monnaire,
            "durree": self.durree,
        }

    def __repr__(self):
        return f'<PlanTarification  {self.id}>'
    



class ActeurDomaines(db.Model):
    __tablename__="ActeurDomaines"
    acteur_id = db.Column(db.Integer, db.ForeignKey('Users.id'),primary_key=True)  # Foreign key reference
    interet_id = db.Column(db.Integer, db.ForeignKey('InterestDomaines.id'),primary_key=True)  # Foreign key reference


    def __repr__(self):
        return f'<ActeurDomaine {self.id}>'


class InterestDomaines(db.Model) :
    __tablename__="InterestDomaines"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)

    
    def __repr__(self):
        return f'<InterestDomaine {self.id}>'