from flask import Flask
from marshmallow.exceptions import ValidationError
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.trainer_controller import trainer_bp
from controllers.member_controller import member_bp
from controllers.gymclass_controller import gymclass_bp
from controllers.auth_controller import auth_bp
from controllers.classlog_controller import classlog_bp


def create_app():
    # Create flask app object
    app = Flask(__name__)

    # Sort schema attributes
    app.json.sort_keys = False

    # Setup environment
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Error handling
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {'error':str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    # Initialise
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(trainer_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(gymclass_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(classlog_bp)
    
    return app