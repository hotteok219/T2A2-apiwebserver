from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from datetime import timedelta
from init import db, bcrypt
from models.trainers import Trainer, trainer_schema, trainers_schema, trainerpw_schema


trainer_bp = Blueprint('trainer', __name__, url_prefix='/trainer')


# Show list of trainers - no auth required
@trainer_bp.route('/')
def trainer_list():
    stmt = db.select(Trainer)
    trainers = db.session.scalars(stmt)

    # Return list of trainers' details
    return trainers_schema.dump(trainers)



# Show specific trainer - no auth required
@trainer_bp.route('/<int:id>')
def trainer_id(id):
    # Look for trainer with id
    stmt = db.select(Trainer).filter_by(id=id)
    trainer = db.session.scalar(stmt)

    # If trainer exists, return trainer details
    if trainer:
        return trainer_schema.dump(trainer)
    # If trainer doesn't exist, return error
    else:
        return {'error': f'Trainer with id {id} does not exist.'}, 404



# Register a trainer - auth required: trainers only
@trainer_bp.route('/register', methods=['POST'])
@jwt_required()
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
        # Set an expiry on the token
        token = create_access_token(identity=str(trainer.id), expires_delta=timedelta(days=1))
        return {'email': trainer.email, 'token': token}
    # If trainer doesn't exist, return error
    else:
        return {'error': 'Invalid email or password.'}, 401



# Delete a trainer - auth required: trainers only
@trainer_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def trainer_delete(id):
    # Look for trainer with id
    stmt = db.select(Trainer).filter_by(id=id)
    trainer = db.session.scalar(stmt)

    # If trainer exists, delete trainer
    if trainer:
        db.session.delete(trainer)
        db.session.commit()
        return {'message': f'Trainer with id {id} removed successfully.'}
    else:
        return {'error': f'Trainer with id {id} does not exist.'}, 404



# Update a trainer - auth required: any trainer can update any trainer's details
@trainer_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def trainer_update(id):
    # Obtain data from user input - using trainerpw_schema to enable password updates
    body_data = trainerpw_schema.load(request.get_json(), partial=True)

    # Look for trainer with id
    stmt = db.select(Trainer).filter_by(id=id)
    trainer = db.session.scalar(stmt)

    # If trainer exists, update trainer
    if trainer:
        trainer.first_name = body_data.get('first_name') or trainer.first_name
        trainer.last_name = body_data.get('last_name') or trainer.last_name
        trainer.dob = body_data.get('dob') or trainer.dob
        trainer.phone = body_data.get('phone') or trainer.phone
        trainer.email =  body_data.get('email') or trainer.email
        trainer.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8') or trainer.password
        trainer.emergency_contact_name =  body_data.get('emergency_contact_name') or trainer.emergency_contact_name
        trainer.emergency_contact_phone = body_data.get('emergency_contact_phone') or trainer.emergency_contact_phone
        trainer.first_aid_officer = body_data.get('first_aid_officer') or trainer.first_aid_officer

        db.session.commit()
        # Respond to client without showing the password
        return trainer_schema.dump(trainer)
    else:
        return {'error': f'Trainer with id {id} does not exist.'}, 404