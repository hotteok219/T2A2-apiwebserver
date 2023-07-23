from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.trainer_controller import trainer_bp
from controllers.member_controller import member_bp
from controllers.class_controller import gymclass_bp
from controllers.auth_controller import auth_bp

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

    app.register_blueprint(db_commands)
    app.register_blueprint(trainer_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(gymclass_bp)
    app.register_blueprint(auth_bp)
    
    return app