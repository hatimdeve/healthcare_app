from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, current_user, login_required,LoginManager,login_user,UserMixin
from flask import jsonify
import plotly.graph_objs as go
import random
# Importing models
from models import db,Patient,Infirmier,Soin,Dossier,Notificationpatient,Notificationinfermier
from controller import PatientDao,InfermierDao
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
login_manager = LoginManager(app)
login_manager.login_view = 'login'
starti=1
endi=5
startp=1
endp=5
notificationpatient={}
notificationinfermier={}
notifcountpatient=0
notifcountinfermier=0
@login_manager.user_loader
def load_user(user_id):
    # Check if the user_id corresponds to a Patient or an Infirmier
    patient = Patient.query.get(user_id)
    if patient:
        return patient
    infirmier = Infirmier.query.get(user_id)
    if infirmier:
        return infirmier
    # If user_id does not correspond to any user, return None
    return None
# Initialize db with app
db.init_app(app)
# Create all database tables when the application starts
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

    # Print the schema
    print("Database schema:")
    for table_name, table in db.metadata.tables.items():
        print(f"Table: {table_name}")
        for column in table.columns:
            print(f"- Column: {column.name} ({column.type})")

            # Check if the column is a foreign key
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    print(f"  - Foreign Key: {fk.column} ({fk.column.type}) -> {fk.column.table}")
    existing_soins = Soin.query.all()

    if not existing_soins:  # If no existing records are found, insert the data
       # Create new Soin instances
       soin1 = Soin(nom_s='Administration de médicaments', prix=50)
       soin2 = Soin(nom_s='Soins des plaies', prix=100)
       soin3 = Soin(nom_s='Surveillance des signes vitaux', prix=80)
       soin4 = Soin(nom_s='Soins de stomie', prix=90)
       soin5 = Soin(nom_s='Soins injections', prix=110)
       soin6 = Soin(nom_s='Soins de cathéter', prix=3000)
       soin7 = Soin(nom_s='Soins de trachéotomie', prix=2000)
       soin8 = Soin(nom_s='Soins de plaies chroniques', prix=800)
       soin9 = Soin(nom_s='Soins de nutrition entérale', prix=40)
       soin10 = Soin(nom_s='Éducation et conseil', prix=220)
    
      # Add the new instances to the session and commit
       db.session.add_all([soin1,soin2,soin3,soin4,soin5,soin6,soin7,soin8,soin9,soin10])
       db.session.commit()

       print("Soin records inserted successfully.")
    else:
       print("Soin records already exist in the database.")

   
print("Values inserted into the 'soins' table successfully.")
@app.route('/')
def index():
     return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        patient = Patient.query.filter_by(email=email).first()
        infermier = Infirmier.query.filter_by(email=email).first()
        if patient and check_password_hash(patient.mdp, password):
            login_user(patient)  # Log in the user
            user=get_user_type(current_user.get_id())
            notifications_content = Notificationpatient.query.filter_by(idp=current_user.get_id()).all()
            notifcountpatient=len(notifications_content)
            return render_template('dashbordpatient.html',user=user,userr=current_user.get_id(),notificationpatient=notificationpatient,notifcountpatient=notifcountpatient)
        if infermier and check_password_hash(infermier.mdp, password):
            login_user(infermier)  # Log in the user
            user=get_user_type(current_user.get_id())
            notifications_content = Notificationinfermier.query.filter_by(idf=current_user.get_id()).all()
            notifcountinfermier=len(notifications_content)
            return render_template('dashbordinfermier.html',user=user,notificationinfermier=notificationinfermier,notifcountinfermier=notifcountinfermier)
        

    return render_template('login.html')
@app.route('/register_infermier', methods=['GET', 'POST'])
def register_infermier():
    global starti,endi
    nombre = random.randint(starti, endi)  # Génère un nombre aléatoire entre 1 et 100
    if nombre % 2 != 0:  # Vérifie si le nombre est impair
        nombre += 1  # Ajoute 1 pour le rendre pair
    starti+=5
    endi+=5
    if request.method == 'POST':
        nom=request.form['nom']
        prenom=request.form['prenom']
        email = request.form['email']
        phone_number = request.form['phone_number']
        
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        

        new_infermier = Infirmier(idi=nombre,nom=nom,prenom=prenom,phone_number=phone_number,email=email, mdp=password)
        print(InfermierDao.register_infermier(new_infermier))
        

        return redirect(url_for('login'))

    return render_template('register_infermier.html')
                    
@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    global startp,endp
    nombre = random.randint(startp, endp)  # Génère un nombre aléatoire entre 1 et 100
    if nombre % 2 == 0:  # Vérifie si le nombre est impair
        nombre += 1  # Ajoute 1 pour le rendre pair
    startp+=5
    endp+=5
    if request.method == 'POST':
        nom=request.form['nom']
        prenom=request.form['prenom']
        email = request.form['email']
        adresse=request.form['adresse']
        phone_number=request.form['phone_number']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        

        new_patient = Patient(idp=nombre,nom=nom,prenom=prenom,email=email,adresse=adresse, mdp=password,phone_number=phone_number)
        print(PatientDao.register_patient(new_patient))
        

        return redirect(url_for('login'))

    return render_template('register_patient.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if get_user_type(current_user.get_id())=='patient':
            user=get_user_type(current_user.get_id())
            notifications_content = Notificationpatient.query.filter_by(idp=current_user.get_id()).all()
            notifcountpatient=len(notifications_content)
            return render_template('dashbordpatient.html',user=user,userr=current_user.get_id(),notificationpatient=notificationpatient,notifcountpatient=notifcountpatient)
    elif get_user_type(current_user.get_id())=='infirmier':
            user=get_user_type(current_user.get_id())
            notifications_content = Notificationinfermier.query.filter_by(idf=current_user.get_id()).all()
            notifcountinfermier=len(notifications_content)
           # Retrieve dossier count and total amount for the current user (infirmier) from the database
            infirmier = Infirmier.query.filter_by(idi=current_user.get_id()).first()
            dossier_count = Dossier.query.join(Infirmier).filter(Infirmier.idi == infirmier.idi, Dossier.status == 'dossier_traiter').count()
            total_money = Soin.query.join(Dossier).join(Infirmier).filter(Infirmier.idi == infirmier.idi, Dossier.status == 'dossier_traiter').with_entities(Soin.prix).all()
            # print(dossier_count)
            money_made = sum(amount for (amount,) in total_money)
            print(money_made)
    # Create Plotly bar charts
            dossier_data = [
        go.Bar(
            x=[infirmier.nom],
            y=[dossier_count],
            name='Dossiers',
            marker=dict(color='rgb(26, 118, 255)')
        )
    ]
            dossier_layout = go.Layout(
        title='Treated Dossiers Count for User',
        xaxis=dict(title='User'),
        yaxis=dict(title='Dossier Count')
    )
            dossier_chart = go.Figure(data=dossier_data, layout=dossier_layout)

            amount_data = [
        go.Bar(
            x=[infirmier.nom],
            y=[money_made],
            name='Total Amount',
            marker=dict(color='rgb(255, 87, 51)')
        )
    ]
            amount_layout = go.Layout(
        title='Total Amount for User',
        xaxis=dict(title='User'),
        yaxis=dict(title='Total Amount')
    )
            amount_chart = go.Figure(data=amount_data, layout=amount_layout)

    # Convert the Plotly charts to JSON
            dossier_chart_json = dossier_chart.to_json()
            money_chart_json = amount_chart.to_json()

    # Render the template with the chart data
            return render_template('dashbordinfermier.html',user=user,notificationinfermier=notificationinfermier,notifcountinfermier=notifcountinfermier,chart_json=dossier_chart_json,money_chart_json=money_chart_json)


@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    userr = None
    if Patient.query.filter_by(idp=current_user.get_id()).first() is not None:
        userr=Patient.query.filter_by(idp=current_user.get_id()).first()
        user=get_user_type(current_user.get_id())
        notifications_content = Notificationpatient.query.filter_by(idp=current_user.get_id()).all()
        notifcountpatient=len(notifications_content)
        return render_template('profilepatient.html', userr=userr,user=user,notificationpatient=notificationpatient,notifcountpatient=notifcountpatient)
    elif Infirmier.query.filter_by(idi=current_user.get_id()).first() is not None:
        userr=Infirmier.query.filter_by(idi=current_user.get_id()).first()
        notifications_content = Notificationinfermier.query.filter_by(idf=current_user.get_id()).all()
        notifcountinfermier=len(notifications_content)
        user=get_user_type(current_user.get_id())
        return render_template('profileinfermier.html', userr=userr,user=user,notificationinfermier=notificationinfermier,notifcountinfermier=notifcountinfermier)

    
    
def get_user_type(user_id):
   
    
    if Patient.query.filter_by(idp=user_id).first() is not None:
        return 'patient'
    elif Infirmier.query.filter_by(idi=user_id).first() is not None :
        return 'infirmier'
    else:
        return None
    
@app.route('/dossier')
@login_required
def dossier():
    global notifcountpatient,notifcountinfermier
    user=get_user_type(current_user.get_id())
    print(current_user.get_id())
    if Patient.query.filter_by(idp=current_user.get_id()).first() is not None:
       dossiers = Dossier.query.join(Patient, Dossier.idp == Patient.idp).join(Infirmier, Dossier.idf == Infirmier.idi).join(Soin, Dossier.ids == Soin.ids).filter(Patient.idp == current_user.get_id()).all()
       notifications_content = Notificationpatient.query.filter_by(idp=current_user.get_id()).all()
       notifcountpatient=len(notifications_content)
    elif Infirmier.query.filter_by(idi=current_user.get_id()).first() is not None:
        dossiers = Dossier.query.join(Patient, Dossier.idp == Patient.idp).join(Infirmier, Dossier.idf == Infirmier.idi).join(Soin, Dossier.ids == Soin.ids).filter(Infirmier.idi == current_user.get_id()).all()
        notifications_content = Notificationinfermier.query.filter_by(idf=current_user.get_id()).all()
        notifcountinfermier=len(notifications_content)
    available_nurses = Infirmier.query.filter_by(isdipo=True).all()  
    treatments = Soin.query.all()  
    return render_template('dossier.html', dossiers=dossiers,user=user,available_nurses=available_nurses,soin=treatments,notificationpatient=notificationpatient,notifcountpatient=notifcountpatient,notificationinfermier=notificationinfermier,notifcountinfermier=notifcountinfermier)

@app.route('/update_status/<int:dossier_id>', methods=['GET','POST'])
@login_required
def update_status(dossier_id):
    global notifcountpatient
    # Get the new status from the request form data
    new_status = "accecpt_par_infermier"

    # Find the dossier by ID
    dossier = Dossier.query.get(dossier_id)
    if not dossier:
        return jsonify({'error': 'Dossier not found'}), 404

    # Update the status
    dossier.status = new_status



     # Create a new dossier instance
    new_notif = Notificationpatient(idp=dossier.idp, content="linfermier a"+dossier.infirmier.nom+"accepter votre dossier veilliez payer svp")

    # Add the new dossier to the database session
    db.session.add(new_notif)
  

    
    # Commit the changes to the database
    db.session.commit()
    

    return redirect(url_for('dossier'))

@app.route('/get_notifications_patients', methods=['GET'])
def get_notifications_patients():
        global notificationpatient
        notifications_content = Notificationpatient.query.filter_by(idp=current_user.get_id()).all()
        notifications_data_patient = [notification.to_dict() for notification in notifications_content]
        notificationpatient=notifications_data_patient
        print(notifications_data_patient)
        return jsonify(notifications_data_patient)
@app.route('/get_notifications_infermiers', methods=['GET'])
def get_notifications_infermiers():
        global notificationpatient
        notifications_content = Notificationinfermier.query.filter_by(idf=current_user.get_id()).all()
        notifications_data_infermier = [notification.to_dict() for notification in notifications_content]
        notificationpatient=notifications_data_infermier
        print(notifications_data_infermier)
        return jsonify(notifications_data_infermier)
@app.route('/dismiss_notification/<int:notification_id>', methods=['GET','DELETE'])
@login_required
def dismiss_notification(notification_id):
    global notifcountpatient
    try:
        notification = Notificationpatient.query.get(notification_id)
        notifcountpatient-=1
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return jsonify({'message': 'Notification dismissed successfully', 'reload': True}), 200
        else:
            return jsonify({'message': 'Notification not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500   

@app.route('/dismiss_notification_inf/<int:notification_id>', methods=['GET','DELETE'])
@login_required
def dismiss_notification_inf(notification_id):
    global notifcountinfermier
    try:
        notification = Notificationinfermier.query.get(notification_id)
        notifcountinfermier-=1
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return jsonify({'message': 'Notification dismissed successfully', 'reload': True}), 200
        else:
            return jsonify({'message': 'Notification not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500     
@app.route('/payer/<int:dossier_id>', methods=['GET','POST'])
@login_required
def payer(dossier_id):
    # Get the new status from the request form data
    new_status = "payer_par_client"

    # Find the dossier by ID
    dossier = Dossier.query.get(dossier_id)
    if not dossier:
        return jsonify({'error': 'Dossier not found'}), 404

    # Update the status
    dossier.status = new_status
    dossier.infirmier.isdipo= False
    # Commit the changes to the database
    db.session.commit()

    return redirect(url_for('dossier'))
@app.route('/finaliser_soin/<int:dossier_id>', methods=['GET','POST'])
@login_required
def finaliser_soin(dossier_id):
    # Get the new status from the request form data
    new_status = "dossier_traiter"

    # Find the dossier by ID
    dossier = Dossier.query.get(dossier_id)
    if not dossier:
        return jsonify({'error': 'Dossier not found'}), 404

    # Update the status
    dossier.status = new_status
    dossier.infirmier.isdipo= True
    # Commit the changes to the database
    db.session.commit()

    return redirect(url_for('dossier'))

@app.route('/update_patient/<int:user_id>', methods=['GET','POST'])
@login_required
def update_patient(user_id):
    nom=request.form['nom']
    prenom=request.form['prenom']
    adresse=request.form['adresse']
    phone_number=request.form['phone_number']
    atc=request.form.getlist('atc')
    dossier = Patient.query.get(user_id)
    dossier.nom=nom
    dossier.prenom=prenom
    dossier.adresse=adresse
    dossier.phone_number=phone_number
    dossier.atc=atc    
     # Commit the changes to the database
    db.session.commit()


    return redirect(url_for('profile'))
@app.route('/view_details/<int:dossier_id>', methods=['GET','POST'])
@login_required
def view_details(dossier_id):
    # Get the new status from the request form data
    new_status = "dossier_traiter"

    # Find the dossier by ID
    dossier = Dossier.query.get(dossier_id)
    if not dossier:
        return jsonify({'error': 'Dossier not found'}), 404

    # Update the status
    dossier.status = new_status
    dossier.infirmier.isdipo= True
    # Commit the changes to the database
    db.session.commit()

    return redirect(url_for('dossier'))
@app.route('/update_dossier/<int:dossier_id>', methods=['POST'])
@login_required
def update_dossier(dossier_id):
    # Get the new status from the request form data
    infirmier_id = request.form['infirmier_id']
    soin_id = request.form['soin_id']
    commentaire_patient = request.form['commentaire_patient']
    dossier = Dossier.query.get(dossier_id)
    # Update the dossier information
    dossier.idf = infirmier_id
    dossier.ids = soin_id
    dossier.commentaire_patient =commentaire_patient
     # Commit the changes to the database
    db.session.commit()


    return redirect(url_for('dossier'))

@app.route('/add_atc/<int:user_id>', methods=['POST'])
def add_atc(user_id):
    if request.method == 'POST':
        # Retrieve the selected ATC values from the form
        atc_values = request.form.getlist('atc')
        print(atc_values)
        # Now you have the selected ATC values, you can process them further
        # For example, you can store them in your database or perform any other action
        patient=Patient.query.get(user_id)
        # Here, we are just printing the selected values for demonstration purposes
        # Assign the selected ATC values to the atc column
        patient.atc = atc_values
        # Add the new patient to the database session
        # Commit the session to save changes to the database
        db.session.commit()
        # You can redirect to another page or render a template as per your requirement
        return redirect(url_for('dashboard'))
    
@app.route('/update_infermier/<int:user_id>', methods=['POST'])
@login_required
def update_infermier(user_id):
    nom=request.form['nom']
    prenom=request.form['prenom']
    phone_number=request.form['phone_number']
    dossier = Infirmier.query.get(user_id)
    dossier.nom=nom
    dossier.prenom=prenom
    dossier.phone_number=phone_number
     
     # Commit the changes to the database
    db.session.commit()


    return redirect(url_for('profile'))

@app.route('/delete_dossier/<int:dossier_id>', methods=['GET','POST'])
@login_required
def delete_dossier(dossier_id):
    # Find the dossier by ID
    dossier = Dossier.query.get(dossier_id)
    if not dossier:
        flash('Dossier not found', 'error')
        return redirect(url_for('dossier'))

    # Delete the dossier from the database
    db.session.delete(dossier)
    db.session.commit()

    flash('Dossier deleted successfully', 'success')
    return redirect(url_for('dossier'))
@app.route('/get_available_nurses')
def get_available_nurses():
    available_nurses = Infirmier.query.filter_by(isdipo=True).all()
    nurse_info = [{'id': nurse.idi, 'nom': nurse.nom, 'prenom': nurse.prenom} for nurse in available_nurses]
    return jsonify({'nurses': nurse_info})
@app.route('/get_available_treatments')
def get_available_treatments():
    treatments = Soin.query.all()
    treatment_info = [{'id': treatment.ids, 'nom_s': treatment.nom_s} for treatment in treatments]
    return jsonify({'treatments': treatment_info})
@app.route('/add_dossier', methods=['POST'])
def add_dossier():
    global notifcountinfermier
    # Get form data
    infirmier_id = request.form['infirmier_id']
    soin_id = request.form['soin_id']
    commentaire_patient = request.form['commentaire_patient']

    # Create a new dossier instance
    new_dossier = Dossier(idp=current_user.idp, idf=infirmier_id, ids=soin_id, status="fait_par_patient", commentaire_patient=commentaire_patient)

    # Add the new dossier to the database session
    db.session.add(new_dossier)
   # Create a new dossier instance
    new_notif = Notificationinfermier(idf=new_dossier.idf, content="lepatient  "+current_user.nom+"a  fait un doosier")

    # Add the new dossier to the database session
    db.session.add(new_notif)
    
    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response indicating success
    return redirect(url_for('dossier'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)