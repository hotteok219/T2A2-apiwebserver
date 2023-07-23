from flask import Blueprint, request
from flask_jwt_extended import jwt_required, create_access_token
from datetime import timedelta
from init import db, bcrypt
from controllers.trainer_controller import trainer_bp
from controllers.member_controller import member_bp
from models.trainers import Trainer, trainer_schema, trainers_schema
from models.members import Member, member_schema, members_schema
from decorators.auth_decorator import authorise_as_trainer


auth_bp = Blueprint('auth', __name__)


# Register a trainer - auth required: trainers only
@trainer_bp.route('/register', methods=['POST'])
@jwt_required()
@authorise_as_trainer
def trainer_register():
    # Obtain data from user input
    body_data = request.get_json()

    # Create a new instance of the Trainer model
    trainer = Trainer()
    trainer.first_name = body_data.get('first_name')
    trainer.last_name = body_data.get('last_name')
    trainer.dob = body_data.get('dob')
    trainer.phone = body_data.get('phone')
    trainer.email =  body_data.get('email')
    if body_data.get('password'):
        trainer.password =  bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
    trainer.emergency_contact_name =  body_data.get('emergency_contact_name')
    trainer.emergency_contact_phone = body_data.get('emergency_contact_phone')
    trainer.first_aid_officer = body_data.get('first_aid_officer')

    # Add trainer to session
    db.session.add(trainer)
    # Commit trainer to session
    db.session.commit()
    # Respond to the user
    return trainer_schema.dump(trainer), 201


# Login as a trainer
@trainer_bp.route('/login', methods=['POST'])
def trainer_login():
    # Obtain data from user input
    body_data = request.get_json()

    # Find the trainer using email address
    stmt = db.select(Trainer).filter_by(email=body_data.get('email'))
    trainer = db.session.scalar(stmt)

    # Check if trainer exists, if yes, check password is correct
    if trainer and bcrypt.check_password_hash(trainer.password, body_data.get('password')):
        # Create a token and set an expiry date
        token = create_access_token(identity=('trainer'+str(trainer.id)), expires_delta=timedelta(days=1))
        return {'email': trainer.email, 'token': token}
    # If trainer doesn't exist, return error
    else:
        return {'error': 'Invalid email or password.'}, 401
    

# Register a member - auth required: trainers only
@member_bp.route('/register', methods=['POST'])
@jwt_required()
@authorise_as_trainer
def member_register():
    # Obtain data from user input
    body_data = request.get_json()

    # Create a new instance of the Member model
    member = Member()
    member.first_name = body_data.get('first_name')
    member.last_name = body_data.get('last_name')
    member.dob = body_data.get('dob')
    member.phone = body_data.get('phone')
    member.email =  body_data.get('email')
    if body_data.get('password'):
        member.password =  bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
    member.emergency_contact_name =  body_data.get('emergency_contact_name')
    member.emergency_contact_phone = body_data.get('emergency_contact_phone')

    # Add member to session
    db.session.add(member)
    # Commit member to session
    db.session.commit()
    # Respond to the user
    return member_schema.dump(member), 201


# Login as a member
@member_bp.route('/login', methods=['POST'])
def member_login():
    # Obtain data from user input
    body_data = request.get_json()

    # Find the member using email address
    stmt = db.select(Member).filter_by(email=body_data.get('email'))
    member = db.session.scalar(stmt)

    # Check if member exists, if yes, check password is correct
    if member and bcrypt.check_password_hash(member.password, body_data.get('password')):
        # Create a token and set an expiry date
        token = create_access_token(identity=('member'+str(member.id)), expires_delta=timedelta(days=1))
        # Return information to the user
        return {'email': member.email, 'token': token}
    # If member doesn't exist, return error
    else:
        return {'error': 'Invalid email or password.'}, 401