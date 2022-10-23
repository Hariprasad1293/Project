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

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hari:roots@localhost:3306/flask_appointmentms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'

db = SQLAlchemy(app)


class AppointmentMs(db.Model):
    __tablename__ = 'appointments'

    appointment_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    demail = db.Column(db.String(50), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    appointment_status = db.Column(db.String(50))


class PaymentMsSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = AppointmentMs
        sqla_session = db.session

    appointment_id = fields.Number(dump_only=True)
    email = fields.String(required=True)
    demail = fields.String(required=True)
    appointment_date = fields.Date(required=True)
    appointment_time = fields.String(required=True)
    appointment_status = fields.String(required=True)



@app.route('/api/bookappointment/', methods=['POST'])
def bookappointment():
    data = request.get_json()
    

    new_appointment = AppointmentMs(email=data['email'], demail=data['demail'], 
    appointment_date=data['appointment_date'], appointment_time=data['appointment_time'], appointment_status="Booked")

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'You have Booked appointment successfully', 'data': data})

@app.route('/api/appointmentstatus/', methods=["GET"])
def appointmentstatus():
    data = request.get_json()
    appointment = AppointmentMs.query.filter_by(email=data['email']).first()

    if not appointment:
        return jsonify({'message': 'Your Did not made any payment'})
    
    appointment_data={}
    appointment_data['appointment_id'] = appointment.appointment_id
    appointment_data['email'] = appointment.email
    appointment_data['demail'] = appointment.demail
    appointment_data['appointment_date'] = appointment.appointment_date
    appointment_data['appointment_time'] = appointment.appointment_time
    appointment_data['appointment_status'] = appointment.appointment_status
    return jsonify({'appointment': appointment_data})

@app.route('/api/appointmentsview/', methods=['GET'])
def appointments_view():
    data = request.get_json()
    print("The data", data)
    email = data['email']
    all_filters = [AppointmentMs.email == email] #
    if request.method == 'GET':
        #appointments = AppointmentMs.query.all()
        #appointments = AppointmentMs.
        # appointments = db.session.query(AppointmentMs.email).filter(email).all() #
        appointments = db.session.query(AppointmentMs).filter(AppointmentMs.email == email).all() # 1
        app_data = PaymentMsSchema().dump(appointments, many=True)
        print(app_data)
        headers = {
    'content-type': "application/json"
    }
        #return app_data
        #return make_response(jsonify(app_data), 200)
        resp =  jsonify({'appointments': app_data})
        #return make_response(jsonify(appointments), 200)
        #resp =  Response(json.dumps(app_data), status=200)
        return resp


@app.route('/api/doctorsappointmentsview/', methods=['GET'])
def doctorsappointments_view():
    data = request.get_json()
    print("The data", data)
    demail = data['demail']
    all_filters = [AppointmentMs.email == demail] #
    if request.method == 'GET':
        #appointments = AppointmentMs.query.all()
        #appointments = AppointmentMs.
        # appointments = db.session.query(AppointmentMs.email).filter(email).all() #
        appointments = db.session.query(AppointmentMs).filter(AppointmentMs.demail == demail).all() # 1
        app_data = PaymentMsSchema().dump(appointments, many=True)
        print(app_data)
        headers = {
    'content-type': "application/json"
    }
        #return app_data
        #return make_response(jsonify(app_data), 200)
        resp =  jsonify({'appointments': app_data})
        #return make_response(jsonify(appointments), 200)
        #resp =  Response(json.dumps(app_data), status=200)
        return resp


    
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=9000, host="0.0.0.0", use_reloader=False)