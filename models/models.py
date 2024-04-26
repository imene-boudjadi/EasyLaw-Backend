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
    infoContact = db.relationship('InfoContact', backref='actor', lazy=True, cascade='all, delete-orphan')

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
    
class InfoContact(db.Model):
    __tablename__ = "InfoContacts"
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<InfoContact {self.id}>'


class Service(db.Model):
    __tablename__ = "Services"
    id = db.Column(db.Integer, primary_key=True)
    nomService = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pic = db.Column(db.String(255), nullable=False)

    
    def __repr__(self):
        return f'<Service {self.id}>'


class AbonementService(db.Model):
    __tablename__ = "AbonementServices"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    durree = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    service_id = db.relationship('Services', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AbonementService {self.id}>'


class Payement(db.Model):
    __tablename__ = "Payements"
    id = db.Column(db.Integer, primary_key=True)
    abonement_id = db.relationship('AbonementService', backref='abonement', lazy=True, cascade='all, delete-orphan')
    plan_tarification = db.relationship('PlanTarifications', backref='plan', lazy=True, cascade='all, delete-orphan')
    moyen_payment = db.Column(db.String(255), nullable=False)
    acteur_id = db.relationship('Users', backref='acteur', lazy=True, cascade='all, delete-orphan')
    date_paiement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payement  {self.id}>'


class PlanTarifications(db.Model):
    __tablename__="PlanTarifications"
    id = db.Column(db.Integer, primary_key=True)
    abonement_id = db.relationship('AbonementService', backref='abonement', lazy=True, cascade='all, delete-orphan')
    nom = db.Column(db.String(255), nullable=False)
    tarif = db.Column(db.Float, nullable=False)
    type_tarification = db.Column(db.String(255), nullable=False)
    monnaire = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<PlanTarification  {self.id}>'
    



class ActeurDomaine(db.Model):
    __tablename__="ActeurDomaines"
    id = db.Column(db.Integer, primary_key=True)
    acteur = db.relationship('Users', backref='acteur', lazy=True, cascade='all, delete-orphan')
    interest_domain = db.relationship('InterestDomaine', backref='interest', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return f'<ActeurDomaine {self.id}>'


class InterestDomaine(db.Model) :
    __tablename__="InterestDomaines"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)

    
    def __repr__(self):
        return f'<InterestDomaine {self.id}>'

