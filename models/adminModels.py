from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .. import db

class infoContact(db.Model):
    __tablename__="infoContact"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    designation=db.Column(db.String)
    value=db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'designation': self.designation,
            'value': self.value
        }
    
  
class Acteur(db.Model):
    __tablename__ = "Acteur"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userName = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    infoContact = db.Column(db.Integer, db.ForeignKey('infoContact.id'))

    role = db.Column(db.String)
    deleted = db.Column(db.Boolean)
    Email = db.Column(db.String(120), index=True, unique=True)


class service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom= db.Column(db.String(64), index=True, unique=True)
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

    




class payement(db.Model):
    __tablename__="payement"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('AbonnementService.id'))
    acteur_id = db.Column(db.Integer, db.ForeignKey('Acteur.id'))
    plan_tarification = db.Column(db.Integer, db.ForeignKey('PlanTarification.id'))

    moyen_paiement=db.Column(db.String)
    date_paiement=db.Column(db.String)

   

