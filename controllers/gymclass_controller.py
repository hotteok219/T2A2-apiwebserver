from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from init import db
from models.gymclasses import GymClass, gymclass_schema, gymclasses_schema
from decorators.auth_decorator import authorise_as_trainer


gymclass_bp = Blueprint('gymclass', __name__, url_prefix='/class')


# Show list of classes - no auth required
@gymclass_bp.route('/')
def gymclass_list():
    stmt = db.select(GymClass)
    gymclasses = db.session.scalars(stmt)

    return gymclasses_schema.dump(gymclasses)


# Show specific class - no auth required
@gymclass_bp.route('/<int:id>')
def gymclass_list_one(id):
    stmt = db.select(GymClass).filter_by(id=id)
    gymclass = db.session.scalar(stmt)

    return gymclass_schema.dump(gymclass)


# Register a class - auth required: trainers only
@gymclass_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_trainer
def gymclass_register():
    # Obtain data from user input
    body_data = request.get_json()

    # Create a new instance of the GymClass model
    gymclass = GymClass()
    gymclass.class_name = body_data.get('class_name')
    gymclass.duration = body_data.get('duration')
    gymclass.day = body_data.get('day')
    gymclass.time = body_data.get('time')
    gymclass.max_cap = body_data.get('max_cap')
    gymclass.trainer_id = body_data.get('trainer_id')

    # Add gymclass to session
    db.session.add(gymclass)
    # Commit gymclass to session
    db.session.commit()
    # Respond to the user
    return gymclass_schema.dump(gymclass), 201


# Delete a class - auth required: trainers only
@gymclass_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_trainer
def gymclass_delete(id):
    # Look for gymclass with id
    stmt = db.select(GymClass).filter_by(id=id)
    gymclass = db.session.scalar(stmt)

    # If gymclass exists, delete gymclass
    if gymclass:
        db.session.delete(gymclass)
        db.session.commit()
        return {'message': f'Class with id {id} removed successfully.'}
    else:
        return {'error': f'Class with id {id} does not exist.'}, 404


# Update a class - auth required: trainers only
@gymclass_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_trainer
def gymclass_update(id):
    # Obtain data from user input
    body_data = gymclass_schema.load(request.get_json(), partial=True)
    
    # Look for gymclass with id
    stmt = db.select(GymClass).filter_by(id=id)
    gymclass = db.session.scalar(stmt)

    # If gymclass exists, update gymclass
    if gymclass:
        gymclass.class_name = body_data.get('class_name') or gymclass.class_name
        gymclass.duration = body_data.get('duration') or gymclass.duration
        gymclass.day = body_data.get('day') or gymclass.day
        gymclass.time = body_data.get('time') or gymclass.time
        gymclass.max_cap = body_data.get('max_cap') or gymclass.max_cap
        gymclass.trainer_id = body_data.get('trainer_id') or gymclass.trainer_id

        db.session.commit()
        # Respond to user
        return gymclass_schema.dump(gymclass)
    else:
        return {'error': f'Gym class with id {id} does not exist.'}, 404