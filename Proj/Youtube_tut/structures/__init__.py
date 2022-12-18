from flask import Flask
# from .batsman.batsman import batsman

# from .main.index import main
from routes import emppl as emp_data
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EmployeeModel.sqlite3'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/emp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SECRET_KEY'] = "random string"
    db=SQLAlchemy(app)



    # app.register_blueprint(main,url_prefix='/main')
    # app.register_blueprint(batsman,url_prefix='/batsman')
    # app.register_blueprint(bowler,url_prefix='/bowler')
    app.register_blueprint(emp_data,url_prefix='/emp')

    return app