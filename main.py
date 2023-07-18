from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create database object
db = SQLAlchemy()

def create_app():
    # create flask app object
    app = Flask(__name__)

    # configure app
    app.config.from_object('config.app_config')

    db.init_app(app)
    
    return app