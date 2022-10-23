import requests
import json
from flask import Flask, request, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import jwt
import datetime
from functools import wraps
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hari:roots@localhost:3306/flask_patientms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'

db = SQLAlchemy(app)


class PatientsMs(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100))

class PatientMsSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = PatientsMs
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    gender = fields.String(required=True)
    mobile = fields.String(required=True)
    address = fields.String(required=True)

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
            current_patient = PatientsMs.query.filter_by(email= data['email']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_patient, *args, **kwargs)
    return decorated

@app.route('/api/register/', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_patient = PatientsMs(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
    password=hashed_password, gender=data['gender'], mobile=data['mobile'], address=data['address'])

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'You have successfully registered', 'data': data})
'''
@app.route('/bookappointments', methods=['POST'])
@token_required
def book_appointments(current_patient):
    data = request.get_json()
    url = "http://127.0.0.1:5002/bookappointment"
    headers = {
    'content-type': "application/json"
    }
    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    print(response)
    return 1
'''
'''
@app.route('/patients', methods=['GET'])
@token_required
def get_all_patients(current_patient):
    patients = PatientsMs.query.all()
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
'''

@app.route('/api/yourprofile/', methods=["GET"])
@token_required
def patientprofile(current_patient):
    patient = PatientsMs.query.filter_by(email=current_patient.email).first()

    if not patient:
        return jsonify({'message': 'Your Account Not found'})
    
    patient_data={}
    patient_data['first_name'] = patient.first_name
    patient_data['last_name'] = patient.last_name
    patient_data['email'] = patient.email
    patient_data['mobile'] = patient.mobile
    patient_data['gender'] = patient.gender
    patient_data['address'] = patient.address
    return jsonify({'patient': patient_data})

@app.route('/api/yourappointments/', methods=["GET"])
@token_required
def yourappointments(current_patient):
    patient = PatientsMs.query.filter_by(email=current_patient.email).first()

    if not patient:
        return jsonify({'message': 'Your Account Not found'})
    
    patient_data={}
    patient_data['first_name'] = patient.first_name
    patient_data['last_name'] = patient.last_name
    patient_data['email'] = patient.email
    patient_data['mobile'] = patient.mobile
    patient_data['gender'] = patient.gender
    patient_data['address'] = patient.address

    url = "http://127.0.0.1:9000/api/appointmentsview/"
    headers = {
    'content-type': "application/json"
    }
    response = requests.request("GET", url, data=json.dumps(patient_data), headers=headers)
    #response = requests.request("GET", url, headers=headers)
    #response = requests.request("GET", url, data=json.dumps(patient_data),)
    #a = json.loads(response)
    a = response.json()
    #print(a)
    #print('this', a)


    #return jsonify({'appointments': response})
    return a
'''
@app.route('/patient/<email>', methods=["GET"])
@token_required
def get_one_patient(current_patient, email):
    patient = PatientsMs.query.filter_by(email=email).first()

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
    patient = PatientsMs.query.filter_by(email=email).first()
    if not patient:
        return jsonify({'message': 'No Patient found'})
    
    db.session.delete(email)
    db.session.commit()
    return jsonify({'message': 'Patient data deleted successfully'})
'''


@app.route('/api/login/')
def login():
    auth = request.authorization
    

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify 1', 401, {'WWW-Authenticate': 'Basic realm="login required"'})

    patient = PatientsMs.query.filter_by(email=auth.username).first()
    print(patient)

    if not patient:
        return make_response('Could not verify 2', 401, {'WWW-Authenticate': 'Basic realm="login required"'})

    if check_password_hash(patient.password, auth.password):
        token = jwt.encode({'email': patient.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify 3', 401, {'WWW-Authenticate': 'Basic realm="Login required"'}) 


    
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=9003, host="0.0.0.0", use_reloader=False)