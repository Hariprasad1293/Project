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

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hari:roots@localhost:3306/flask_paymentms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'

db = SQLAlchemy(app)


class PaymentsMs(db.Model):
    __tablename__ = 'payments'

    transaction_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    demail = db.Column(db.String(50), nullable=False)
    payment_type = db.Column(db.String(50))
    mobile = db.Column(db.String(50),nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    payment_status = db.Column(db.String(50))


class PaymentMsSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = PaymentsMs
        sqla_session = db.session

    transaction_id = fields.Number(dump_only=True)
    email = fields.String(required=True)
    demail = fields.String(required=True)
    payment_type = fields.String(required=True)
    mobile = fields.String(required=True)
    appointment_date = fields.Date(required=True)
    appointment_time = fields.String(required=True)
    payment_status = fields.String(required=True)



@app.route('/api/initiatepayment/', methods=['POST'])
def makepayment():
    data = request.get_json()
    

    new_payment = PaymentsMs(email=data['email'], demail=data['demail'], payment_type=data['payment_type'],
    payment_status="Paid",appointment_date=data['appointment_date'], mobile=data['mobile'], appointment_time=data['appointment_time'])

    db.session.add(new_payment)
    db.session.commit()

    app_dict={}
    app_dict['appointment_date'] = data['appointment_date']
    app_dict['appointment_time'] = data['appointment_time']
    app_dict['email'] = data['email']
    app_dict['demail'] = data['demail']
    url = "http://127.0.0.1:9000/api/bookappointment/"
    headers = {
    'content-type': "application/json"
    }
    response = requests.request("POST", url, data=json.dumps(data), headers=headers)

    #return jsonify({'message': 'You have successfully Paid', 'data': data, 'appointment': app_dict})
    return jsonify({'message': 'You have successfully Paid', 'payment details': data})

@app.route('/api/paymentstatus/', methods=["GET"])
def paymentstatus():
    data = request.get_json()
    payment = PaymentsMs.query.filter_by(email=data['email']).first()

    if not payment:
        return jsonify({'message': 'Your Did not made any payment'})
    
    payment_data={}
    payment_data['transaction_id'] = payment.transaction_id
    payment_data['email'] = payment.email
    payment_data['demail'] = payment.demail
    payment_data['payment_type'] = payment.payment_type
    payment_data['appointment_date'] = payment.appointment_date
    payment_data['appointment_time'] = payment.appointment_time
    payment_data['mobile'] = payment.mobile
    payment_data['payment_status'] = payment.payment_status
    return jsonify({'payment': payment_data})





    
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=9004, host="0.0.0.0", use_reloader=False)