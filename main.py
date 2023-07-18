from flask import Flask
import os
from init import db, ma, bcrypt, jwt

# create database object
# db = SQLAlchemy()

def create_app():
    # create flask app object
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # configure app
    # app.config.from_object('config.app_config')

    # initialise
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    return app