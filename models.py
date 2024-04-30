from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, current_user, login_required,LoginManager,login_user,UserMixin
db = SQLAlchemy()
class Patient(UserMixin,db.Model):
    __tablename__ = 'patients'

    idp = db.Column(db.Integer,unique=True, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    email = db.Column(db.String)
    adresse = db.Column(db.String)
    mdp = db.Column(db.String)
    atc = db.Column(db.String)
    # Define the one-to-many relationship to Dossier
    dossiers = db.relationship("Dossier", back_populates="patient")
    notificationpatients = db.relationship("Notificationpatient", back_populates="patient")
    
    __table_args__ = (
        CheckConstraint('idp % 2 != 0', name='check_idp_even'),
    )
    def get_id(self):
        return str(self.idp)

class Infirmier(UserMixin,db.Model):
    __tablename__ = 'infirmiers'

    idi = db.Column(db.Integer,unique=True, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    email = db.Column(db.String)
    mdp = db.Column(db.String)
    isdipo = db.Column(db.Boolean, default=True) 
    # Define the one-to-many relationship to Dossier
    dossiers = db.relationship("Dossier", back_populates="infirmier")
    notificationinfermiers = db.relationship("Notificationinfermier", back_populates="infirmier")
    __table_args__ = (
        CheckConstraint('idi % 2 = 0', name='check_idi_even'),
    )
    def get_id(self):
        return str(self.idi)

class Soin(db.Model):
    __tablename__ = 'soins'

    ids = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom_s = db.Column(db.String)
    prix = db.Column(db.Integer)

class Dossier(db.Model):
    __tablename__ = 'dossiers'

    idd = db.Column(db.Integer, primary_key=True,autoincrement=True)
    idp = db.Column(db.Integer, db.ForeignKey('patients.idp'))
    idf = db.Column(db.Integer, db.ForeignKey('infirmiers.idi'))
    ids = db.Column(db.Integer, db.ForeignKey('soins.ids'))
    status = db.Column(db.String)
    commentaire_patient = db.Column(db.String)
    commentaire_infirmier = db.Column(db.String)
    # Define the many-to-one relationships to Patient and Infirmier
    patient = db.relationship("Patient", back_populates="dossiers")
    infirmier = db.relationship("Infirmier", back_populates="dossiers")
    # Define the many-to-one relationship to Soin
    soin = db.relationship("Soin")

class Notificationpatient(db.Model):
    __tablename__ = 'notificationpatients'

    idnp = db.Column(db.Integer, primary_key=True,autoincrement=True)
    idp = db.Column(db.Integer, db.ForeignKey('patients.idp'))
    content = db.Column(db.String)

    patient = db.relationship("Patient", back_populates="notificationpatients")
    def to_dict(self):
        return {
            'idnp':self.idnp,
            'content': self.content,
            # Add other attributes you want to include in the dictionary
        }
class Notificationinfermier(db.Model):
    __tablename__ = 'notificationinfermiers'

    idni = db.Column(db.Integer, primary_key=True,autoincrement=True)
    idf = db.Column(db.Integer, db.ForeignKey('infirmiers.idi'))
    content = db.Column(db.String)
    infirmier = db.relationship("Infirmier", back_populates="notificationinfermiers")
    def to_dict(self):
        return {
            'idni':self.idni,
            'content': self.content,

            # Add other attributes you want to include in the dictionary
        }    