from flask import Blueprint, jsonify
from flask import request
from patient.utils.responses import response_with
from patient.utils import responses as resp
from patient.models.patients import Patients, PatientSchema
from patient.utils.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jti

from datetime import datetime
from datetime import timedelta
from datetime import timezone

patient_routes = Blueprint("patient_routes", __name__)

@patient_routes.route('/register/', methods=['POST'])
def register():
    try:
        data = request.get_json()
        data['password'] = Patients.generate_hash(data['password'])
        patient_schema = PatientSchema()
        pat = patient_schema.load(data)
        add_pat = Patients(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'], gender=data['gender'], mobile=data['mobile'], address=data['address'])
        Patients.create(add_pat)
        return response_with(resp.SUCCESS_201, value={"Patient": pat})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@patient_routes.route('/login/', methods=['POST'])
def authenticate_patient():
    try:
        data = request.get_json()
        current_pat = Patients.find_by_email(data['email'])
        if not current_pat:
            return response_with(resp.SERVER_ERROR_404)
        if Patients.verify_hash(data['password'], current_pat.password):
            access_token = create_access_token(identity=data['email'])
            return response_with(resp.SUCCESS_201, value={'message': 'Logged in as {}'.format(current_pat.email), "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@patient_routes.route('/logout/', methods=['POST'])
@jwt_required
def logout(fn):
    try:
        data = request.args.get('access_token')
        print(data)
        return response_with(resp.SUCCESS_201, value={'message': 'Success'})
    except Exception as e:
        print(e)
        return response_with(resp.UNAUTHORIZED_403)
@patient_routes.route("/logouts", methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    #db.session.add(TokenBlocklist(jti=jti, created_at=now))
    #db.session.commit()
    return jsonify(msg="JWT revoked")
