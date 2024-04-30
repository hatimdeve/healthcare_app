from typing import List
from models import Patient,Infirmier,db
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class PatientDao:

 @staticmethod
    
 def register_patient(patient: Patient) -> str:

    
    try:
        # Add the user to the session
        db.session.add(patient)
        # Commit the changes to the database
        db.session.commit()
        return "User registered successfully!"
    except Exception as e:
        # Rollback the transaction in case of any error
        db.session.rollback()
        return f"Error registering user: {e}"
    finally:
        # Close the session
        db.session.close()
class InfermierDao:

 @staticmethod
    
 def register_infermier(infermier: Infirmier) -> str:

    
    try:
        # Add the user to the session
        db.session.add(infermier)
        # Commit the changes to the database
        db.session.commit()
        return "User registered successfully!"
    except Exception as e:
        # Rollback the transaction in case of any error
        db.session.rollback()
        return f"Error registering user: {e}"
    finally:
        # Close the session
        db.session.close()
                
        
    