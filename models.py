from . import db
from sqlalchemy import func

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

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