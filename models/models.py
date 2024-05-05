from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .. import db
from enum import Enum
from sqlalchemy import func


class Service(db.Model):
    __tablename__="service"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nomService = db.Column(db.String)
    description = db.Column(db.Text)
    pic = db.Column(db.String)

class PlanTarification(db.Model):
    __tablename__="planTarification"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    type_tarification = db.Column(db.String)
    tarif = db.Column(db.Integer)
    description = db.Column(db.Text)

class Domaine(db.Model):
    __tablename__="domaine"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String)


class RoleEnum(str, Enum):
    user = 'user'
    admin = 'admin'
    moderateur = 'moderateur'
   


    



class Users(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    niveau = db.Column(db.Integer)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    phoneNumber = db.Column(db.Integer)
    email = db.Column(db.String,unique=True)
    deleted = db.Column(db.Boolean,default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return f'<User {self.username} {self.id}>'

    def to_dict(self):
     return {
        'id': self.id,
        'username': self.username,
        'password': self.password,
        'niveau': self.niveau,
        'role': str(self.role),  # Convertir l'énumération en chaîne
        'phoneNumber ': self.phoneNumber ,
        'email': self.email,
        'deleted': self.deleted,
        'created_at': self.created_at
    }



class AccessToken(db.Model):
    __tablename__="accessToken"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Users_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))

    expires = db.Column(db.DateTime)


class AbonnementService(db.Model):
    __tablename__="abonnementService"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    access_token_id = db.Column(db.Integer, db.ForeignKey('accessToken.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('planTarification.id'))
    date_abonnement = db.Column(db.DateTime)


class payement(db.Model):
    __tablename__="payement"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('abonnementService.id'))
    Moyen_paiement = db.Column(db.String)
    date_paiement = db.Column(db.Date)

































































"""
class infoContact(db.Model):
    __tablename__="infoContact"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    designation=db.Column(db.String)
    value=db.Column(db.String)
    Users = db.Column(db.Integer, db.ForeignKey('Users.id'))


    def to_dict(self):
        return {
            'id': self.id,
            'designation': self.designation,
            'value': self.value
        }
    
  
class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userName = db.Column(db.String(64), index=True)
    password = db.Column(db.String(64))
    contacts = db.relationship('infoContact', backref='Usersrelation', lazy='dynamic')

    role = db.Column(db.String)
    deleted = db.Column(db.Boolean)
    Email = db.Column(db.String(120), index=True, unique=True)
    def to_dict(self):
        return {
            'id': self.id,
            'userName': self.userName,
            'password': self.password,
            'role': self.role,
            'deleted': self.deleted,
            'Email': self.Email,
            'contacts': [contact.to_dict() for contact in self.contacts]
        }


class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom= db.Column(db.String(64), index=True)
    description = db.Column(db.String(100))
    pic = db.Column(db.String(100))

    
    
class AbonnementService(db.Model):
    __tablename__ = "AbonnementService"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
   
    nom = db.Column(db.String)
    duree = db.Column(db.Integer)
    description = db.Column(db.String)
    service_id=db.Column(db.Integer, db.ForeignKey('service.id'))

class PlanTarification(db.Model):
    __tablename__ = "PlanTarification"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String)
    type_tarification = db.Column(db.String)
    tarif=db.Column(db.Integer)
    monnaire = db.Column(db.String)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('AbonnementService.id'))

    
class Payement(db.Model):
    __tablename__="payement"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('AbonnementService.id'))
    Users_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    plan_tarification = db.Column(db.Integer, db.ForeignKey('PlanTarification.id'))

    moyen_paiement=db.Column(db.String)
    date_paiement=db.Column(db.String)

   




class ContenuScrape(db.Model):
    __tablename__="ContenuScrape"
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    dateScraping = db.Column(db.Date)
    UsersId = db.Column(db.Integer)
    typeSourceScrape = db.Column(db.Integer)
    indexe = db.Column(db.Boolean)


class SourceScrapingDocument(db.Model):
    __tablename__="SourceScrapingDocument"
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(255))
    typeDocument = db.Column(db.Boolean)
    typeContenu = db.Column(db.String(255))
    idContenu = db.Column(db.Integer, db.ForeignKey('ContenuScrape.id'))


class SourceScrapingWeb(db.Model):
    __tablename__="SourceScrapingWeb"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    typeContenu = db.Column(db.String(255))
    autoScraping = db.Column(db.Boolean)
    frequence = db.Column(db.String(255))
"""

