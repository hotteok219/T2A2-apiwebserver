from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from init import db, bcrypt
from models.trainers import Trainer, trainer_schema, trainers_schema, trainerpw_schema
from decorators.auth_decorator import authorise_as_trainer


trainer_bp = Blueprint('trainer', __name__, url_prefix='/trainer')


# Show list of trainers - auth required: trainers only
@trainer_bp.route('/')
@jwt_required()
@authorise_as_trainer
def trainer_list():
    stmt = db.select(Trainer)
    trainers = db.session.scalars(stmt)

    # Return list of trainers' details
    return trainers_schema.dump(trainers)


# Show specific trainer - auth required: trainers only
@trainer_bp.route('/<int:id>')
@jwt_required()
@authorise_as_trainer
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


# Delete a trainer - auth required: trainers only
@trainer_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_trainer
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
@authorise_as_trainer
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