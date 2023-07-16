from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    # create flask app object
    app = Flask(__name__)

    # configure app
    app.config.from_object("config.app_config")

    # create database object
    db = SQLAlchemy(app)
    
    return app