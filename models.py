from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, CheckConstraint,JSON
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, current_user, login_required,LoginManager,login_user,UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
import base64
db = SQLAlchemy()
class Patient(UserMixin,db.Model):
    __tablename__ = 'patients'

    idp = db.Column(db.Integer,unique=True, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    email = db.Column(db.String)
    adresse = db.Column(db.String)
    mdp = db.Column(db.String)
    phone_number = db.Column(db.String) 
    atc = db.Column(db.JSON)
    # Define the one-to-many relationship to Dossier
    dossiers = db.relationship("Dossier", back_populates="patient")
    demandes = db.relationship("Demande", back_populates="patient")
    notificationpatients = db.relationship("Notificationpatient", back_populates="patient")
    
    # __table_args__ = (
    #     CheckConstraint('idp % 2 != 0', name='check_idp_even'),
    # )
    def get_id(self):
        return str(self.idp)

class Infirmier(UserMixin,db.Model):
    __tablename__ = 'infirmiers'

    idi = db.Column(db.Integer,unique=True, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    spesialiter = db.Column(db.String)
    email = db.Column(db.String)
    mdp = db.Column(db.String)
    phone_number = db.Column(db.String) 
    isdipo = db.Column(db.Boolean, default=True) 
    # Define the one-to-many relationship to Dossier
    dossiers = db.relationship("Dossier", back_populates="infirmier")
    notificationinfermiers = db.relationship("Notificationinfermier", back_populates="infirmier")
    # __table_args__ = (
    #     CheckConstraint('idi % 2 = 0', name='check_idi_even'),
    # )
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
    idm = db.Column(db.Integer, db.ForeignKey('medecins.idm'))
    status = db.Column(db.String)
    examin = db.Column(db.LargeBinary)
    notes_de_medcin = db.Column(db.String)
    # commentaire_patient = db.Column(db.String)
    # commentaire_infirmier = db.Column(db.String)
    # Define the many-to-one relationships to Patient and Infirmier
    patient = db.relationship("Patient", back_populates="dossiers")
    infirmier = db.relationship("Infirmier", back_populates="dossiers")
    medecin = db.relationship("Medecin", back_populates="dossiers")
    # Define the many-to-one relationship to Soin
    soin = db.relationship("Soin")


    @hybrid_property
    def examin_base64(self):
           if self.examin:
             return base64.b64encode(self.examin).decode('utf-8')
           else:
             return None
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

class Notificationmedecin(db.Model):
    __tablename__ = 'notificationmedecins'

    idnm = db.Column(db.Integer, primary_key=True,autoincrement=True)
    idm = db.Column(db.Integer, db.ForeignKey('medecins.idm'))
    content = db.Column(db.String)
    medecin = db.relationship("Medecin", back_populates="notificationmedecins")
    def to_dict(self):
        return {
            'idnm':self.idnm,
            'content': self.content,

            # Add other attributes you want to include in the dictionary
        }     
        7
class Medecin(UserMixin,db.Model):
    __tablename__ = 'medecins'

    idm = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    adresse = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    mdp = db.Column(db.String)
    # Define one-to-many relationship with Dossier
    dossiers = db.relationship("Dossier", back_populates="medecin")    
    demandes = db.relationship("Demande", back_populates="medecin")
    notificationmedecins = db.relationship("Notificationmedecin", back_populates="medecin")   
    def get_id(self):
        return str(self.idm)
    

class Demande(db.Model):
    __tablename__ = 'demandes'

    idde = db.Column(db.Integer, primary_key=True,autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.idp'))
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecins.idm'))
    ids = db.Column(db.Integer, db.ForeignKey('soins.ids'))
    status = db.Column(db.String)
    content = db.Column(db.String)
    # Define relationships
    patient = db.relationship("Patient", back_populates="demandes")
    medecin = db.relationship("Medecin", back_populates="demandes")  
    
    soin = db.relationship("Soin")   