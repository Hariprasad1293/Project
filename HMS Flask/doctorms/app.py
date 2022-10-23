import requests
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

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hari:roots@localhost:3306/flask_doctorms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'

db = SQLAlchemy(app)


class DoctorsMs(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    speciality = db.Column(db.String(50))
    demail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100))

class DoctorsMsSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = DoctorsMs
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    specaility = fields.String(required=True)
    demail = fields.String(required=True)
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
            current_patient = DoctorsMs.query.filter_by(demail= data['demail']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_patient, *args, **kwargs)
    return decorated

@app.route('/api/register/', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_doctor = DoctorsMs(first_name=data['first_name'], last_name=data['last_name'], demail=data['demail'],
    password=hashed_password, speciality=data['speciality'],gender=data['gender'], mobile=data['mobile'], address=data['address'])

    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({'message': 'You have successfully registered', 'data': data})

@app.route('/api/yourprofile/', methods=["GET"])
@token_required
def doctorprofile(current_doctor):
    doctor = DoctorsMs.query.filter_by(demail=current_doctor.demail).first()

    if not doctor:
        return jsonify({'message': 'Your Account Not found'})
    
    doctor_data={}
    doctor_data['first_name'] = doctor.first_name
    doctor_data['last_name'] = doctor.last_name
    doctor_data['email'] = doctor.demail
    doctor_data['speciality'] = doctor.speciality
    doctor_data['mobile'] = doctor.mobile
    doctor_data['gender'] = doctor.gender
    doctor_data['address'] = doctor.address
    return jsonify({'doctor': doctor_data})


@app.route('/api/login/')
def login():
    auth = request.authorization
    

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify 1', 401, {'WWW-Authenticate': 'Basic realm="login required"'})

    doctor = DoctorsMs.query.filter_by(demail=auth.username).first()
   

    if not doctor:
        return make_response('Could not verify 2', 401, {'WWW-Authenticate': 'Basic realm="login required"'})

    if check_password_hash(doctor.password, auth.password):
        token = jwt.encode({'demail': doctor.demail, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify 3', 401, {'WWW-Authenticate': 'Basic realm="Login required"'}) 

@app.route('/api/yourappointments/', methods=["GET"])
@token_required
def yourappointments(current_doctor):
    doctor = DoctorsMs.query.filter_by(demail=current_doctor.demail).first()

    if not doctor:
        return jsonify({'message': 'Your Account Not found'})
    
    doctor_data={}
    doctor_data['first_name'] = doctor.first_name
    doctor_data['last_name'] = doctor.last_name
    doctor_data['demail'] = doctor.demail
    doctor_data['speciality'] = doctor.speciality
    doctor_data['mobile'] = doctor.mobile
    doctor_data['gender'] = doctor.gender
    doctor_data['address'] = doctor.address

    url = "http://127.0.0.1:9000/api/doctorsappointmentsview/"
    headers = {
    'content-type': "application/json"
    }
    response = requests.request("GET", url, data=json.dumps(doctor_data), headers=headers)
    #response = requests.request("GET", url, headers=headers)
    #response = requests.request("GET", url, data=json.dumps(patient_data),)
    #a = json.loads(response)
    a = response.json()
    #print(a)
    #print('this', a)


    #return jsonify({'appointments': response})
    return a
    
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=9002, host="0.0.0.0", use_reloader=False)