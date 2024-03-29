from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db, bcrypt
from models.trainers import Trainer
from schemas.trainer_schema import trainer_schema, trainers_schema, trainerpw_schema
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
def trainer_list_one(id):
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
    try:
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
            # Check if there is user input for a password update
            if body_data.get('password'):
                    # Check if current user is the trainer being queried
                    current_user = get_jwt_identity()
                    if current_user.startswith('trainer') and str(trainer.id) == current_user[7:]:
                        trainer.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
                    else:
                        return {'error': 'Only a trainer can update their own password.'}
            trainer.emergency_contact_name =  body_data.get('emergency_contact_name') or trainer.emergency_contact_name
            trainer.emergency_contact_phone = body_data.get('emergency_contact_phone') or trainer.emergency_contact_phone
            trainer.first_aid_officer = body_data.get('first_aid_officer') or trainer.first_aid_officer

            db.session.commit()
            # Respond to client without showing the password
            return trainer_schema.dump(trainer)
        else:
            return {'error': f'Trainer with id {id} does not exist.'}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'Email address already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required'}, 409