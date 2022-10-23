import json
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import jwt
import datetime
from functools import wraps
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hari:roots@localhost:3306/flask_patientsfinal"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'

db = SQLAlchemy(app)


class AppointmentsDummy(db.Model):
    __tablename__ = 'appointmentsdummy'

    a_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False)
    d_email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100))
    payment_status = db.Column(db.String(100))

class AppointmentSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = AppointmentsDummy
        sqla_session = db.session

    a_id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    d_email = fields.String(required=True)
    gender = fields.String(required=True)
    mobile = fields.String(required=True)
    address = fields.String(required=True)
    payment_status = fields.String(required=True)

'''
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_patient = PatientsDummy.query.filter_by(email= data['email']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_patient, *args, **kwargs)
    return decorated
'''
@app.route('/bookappointment', methods=['POST'])
def register():
    data = request.get_json()
    

    new_appointment = AppointmentsDummy(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
    d_email = data['d_email'], gender = data['gender'], mobile=data['mobile'], address=data['address'], payment_status="Booked")

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'New Appointment Added', 'data': data})

'''
@app.route('/patients', methods=['GET'])
def get_all_patients(current_patient):
    patients = PatientsDummy.query.all()
    output = []
    for patient in patients:
        patient_data = {}
        patient_data['first_name'] = patient.first_name
        patient_data['last_name'] = patient.last_name
        patient_data['email'] = patient.email
        patient_data['mobile'] = patient.mobile
        patient_data['gender'] = patient.gender
        patient_data['address'] = patient.address
        output.append(patient_data)
    return jsonify({'patients': output})

@app.route('/patientprofile', methods=["GET"])
@token_required
def patientprofile(current_patient):
    patient = PatientsDummy.query.filter_by(email=current_patient.email).first()

    if not patient:
        return jsonify({'message': 'No Patient Found'})
    
    patient_data={}
    patient_data['first_name'] = patient.first_name
    patient_data['last_name'] = patient.last_name
    patient_data['email'] = patient.email
    patient_data['mobile'] = patient.mobile
    patient_data['gender'] = patient.gender
    patient_data['address'] = patient.address
    return jsonify({'patient': patient_data})

@app.route('/patient/<email>', methods=["GET"])
@token_required
def get_one_patient(current_patient, email):
    patient = PatientsDummy.query.filter_by(email=email).first()

    if not patient:
        return jsonify({'message': 'No Patient Found'})
    
    patient_data={}
    patient_data['first_name'] = patient.first_name
    patient_data['last_name'] = patient.last_name
    patient_data['email'] = patient.email
    patient_data['mobile'] = patient.mobile
    patient_data['gender'] = patient.gender
    patient_data['address'] = patient.address
    return jsonify({'patient': patient_data})

# not working 
@app.route('/patient/<email>', methods=["DELETE"])
def delete_patient(email):
    patient = PatientsDummy.query.filter_by(email=email).first()
    if not patient:
        return jsonify({'message': 'No Patient found'})
    
    db.session.delete(email)
    db.session.commit()
    return jsonify({'message': 'Patient data deleted successfully'})


@app.route('/logins')
def logins():
    auth = request.authorization
    

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify 1', 401, {'WWW-Authenticate': 'Basic realm="login required"'})

    patient = PatientsDummy.query.filter_by(email=auth.username).first()
    print(patient)

    if not patient:
        return make_response('Could not verify 2', 401, {'WWW-Authenticate': 'Basic realm="login required"'})

    if check_password_hash(patient.password, auth.password):
        token = jwt.encode({'email': patient.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify 3', 401, {'WWW-Authenticate': 'Basic realm="Login required"'}) 


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    error = None

    try:
        #user = db[username]
        patient = PatientsDummy.query.filter_by(email=email).first()
    except:
        patient = None

    if patient is None or not check_password_hash(patient.password, password):
        error = 'Incorrect patient or password'

    if error is None:
        payload = {
            'iat': datetime.datetime.utcnow(),                          # Current time
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),  # Expiration time
            'email': patient.email,
            #'user': user['rol']
        }
        return make_response(jwt.encode(payload, app.config['SECRET_KEY'],algorithm='HS256'), 200)

    return make_response(error, 401)  '''
    



db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5002, host="0.0.0.0", use_reloader=False)