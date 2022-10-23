import os
import logging
import sys
from flask import Flask
from flask import jsonify
from patient.utils.database import db
from patient.utils.responses import response_with
import patient.utils.responses as resp
from patient.routes.patients import patient_routes
from patient.config.config import ProductionConfig, TestingConfig, DevelopmentConfig
from flask_jwt_extended import JWTManager
app = Flask(__name__)
if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig
app.config.from_object(app_config)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all() 

app.register_blueprint(patient_routes, url_prefix='/api')


@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
   logging.error(e)
   return response_with(resp.SERVER_ERROR_404)

db.init_app(app)
with app.app_context():
    db.create_all()
logging.basicConfig(stream=sys.stdout,format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',level=logging.DEBUG)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False) 