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
    infoContact = db.relationship('InfoContacts', backref='users', lazy=True, cascade='all, delete-orphan')
    domaine = db.relationship('InterestDomaines',secondary='ActeurDomaines', backref='users')
    abonment = db.relationship('AbonementServices', backref='users', lazy=True, cascade='all, delete-orphan')

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
    
class InfoContacts(db.Model):
    __tablename__ = "InfoContacts"
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))  # Foreign key reference

    def __repr__(self):
        return f'<InfoContact {self.id}>'


class Services(db.Model):
    __tablename__ = "Services"
    id = db.Column(db.Integer, primary_key=True)
    nomService = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pic = db.Column(db.String(255), nullable=False)
    plan = db.relationship('PlanTarifications', backref='service', lazy=True, cascade='all, delete-orphan')


    @property
    def serialize(self):
        return {
            "id": self.id,
            "nomService": self.nomService,
            "description": self.description
        }
    
    def __repr__(self):
        return f'<Service {self.id}>'


class AbonementServices(db.Model):
    __tablename__ = "AbonementServices"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    durree = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('PlanTarifications.id'))  # Foreign key reference
    date_paiement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    moyen_payment = db.Column(db.String(255), nullable=False)
    acteur_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return f'<AbonementService {self.id}>'



class PlanTarifications(db.Model):
    __tablename__="PlanTarifications"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'))  # Foreign key reference
    nom = db.Column(db.String(255), nullable=False)
    tarif = db.Column(db.Float, nullable=False)
    type_tarification = db.Column(db.String(255), nullable=False)
    monnaire = db.Column(db.String(255), nullable=False)
    durree = db.Column(db.Integer, nullable=False)
    abonement = db.relationship('AbonementServices', backref='plan', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return f'<PlanTarification  {self.id}>'
    



class ActeurDomaines(db.Model):
    __tablename__="ActeurDomaines"
    acteur_id = db.Column(db.Integer, db.ForeignKey('Users.id'),primary_key=True)  # Foreign key reference
    interet_id = db.Column(db.Integer, db.ForeignKey('InterestDomaines.id'),primary_key=True)  # Foreign key reference

    # acteur = db.relationship('Users', backref='acteur', lazy=True, cascade='all, delete-orphan')
    # interest_domain = db.relationship('InterestDomaines', backref='interest', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return f'<ActeurDomaine {self.id}>'


class InterestDomaines(db.Model) :
    __tablename__="InterestDomaines"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)

    
    def __repr__(self):
        return f'<InterestDomaine {self.id}>'

