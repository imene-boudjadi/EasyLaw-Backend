from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .. import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userName = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    bloqued = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    Email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(120), index=True, unique=True)
    
class AbonnementService(db.Model):
    __tablename__ = "AbonnementService"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
   
    planTarification = db.Column(db.Integer)
    
    status = db.Column(db.String)
    Service = db.Column(db.Integer)




class Abonnement_user(db.Model):
    __tablename__ = "abonnement_user"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
   
    Date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('AbonnementService.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

class admins(db.Model):
    __tablename__="admins"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    adminName=db.Column(db.String)
    password=db.Column(db.String)
    level=db.Column(db.Integer)
    Email = db.Column(db.String(120), index=True, unique=True)
    bloqued = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    infos_Contact = db.relationship('infos_Contact', backref='adminbackref', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'adminName': self.adminName,
            'Email': self.Email,
            'level': self.level,
            'bloqued': self.bloqued,
            'deleted': self.deleted,
            'infos_Contact': [contact.to_dict() for contact in self.infos_Contact]
        }

class infos_Contact(db.Model):
    __tablename__="infos_Contact"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    designation=db.Column(db.String)
    value=db.Column(db.String)
    admin=db.Column(db.Integer, db.ForeignKey('admins.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'designation': self.designation,
            'value': self.value
        }
