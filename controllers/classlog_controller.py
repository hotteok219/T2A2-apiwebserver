from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.classlogs import Classlog
from models.gymclasses import GymClass
from schemas.classlog_schema import classlog_schema, classlogs_schema
from decorators.auth_decorator import authorise_as_trainer


classlog_bp = Blueprint('classlog', __name__, url_prefix='/classlog')


# Show class logs - auth required: trainers only
@classlog_bp.route('/')
@jwt_required()
@authorise_as_trainer
def classlog_list():
    stmt = db.select(Classlog)
    classlogs = db.session.scalars(stmt)

    return classlogs_schema.dump(classlogs)


# Show class log of specific entry - auth required: trainers only
@classlog_bp.route('/<int:id>')
@jwt_required()
@authorise_as_trainer
def classlog_list_one(id):
    stmt = db.select(Classlog).filter_by(id=id)
    classlog = db.session.scalar(stmt)

    return classlog_schema.dump(classlog)


# Add an entry to class log - auth required: trainers only
@classlog_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_trainer
def classlog_add():
    try:
        # Obtain data from user input
        body_data = classlog_schema.load(request.get_json())

        # Set up user input for conflict checking
        user_date = body_data.get('date')
        user_time = body_data.get('time')
        user_gymclassid = body_data.get('gymclass_id')    
        user_trainerid = body_data.get('trainer_id') 
        
        # Check if gym class id exists, if not return an error
        gymclass = GymClass.query.get(user_gymclassid)
        if not gymclass:
            return {'error': f'Gym class with id {user_gymclassid} does not exist.'}, 404
        
        # Check for class capacity
        if gymclass.max_cap:
            current_cap = Classlog.query.filter_by(
                gymclass_id=user_gymclassid,
                date=user_date,
                time=user_time
            ).count()
            if current_cap >= gymclass.max_cap:
                return {'error': f'Gym class with id {user_gymclassid} on {user_date} at {user_time} is full. Please try a different class.'}, 400
            
        # Check if a trainer has a conflicting class on the same date and time
        if Classlog.query.filter(
            Classlog.gymclass_id != user_gymclassid,
            Classlog.trainer_id==user_trainerid,
            Classlog.date==user_date,
            Classlog.time==user_time
        ).first():
            return {'error': f'Trainer with id {user_trainerid} is already teaching another class on {user_date} at {user_time}.'}, 400

        # Create a new instance of the Classlog model
        classlog = Classlog()
        classlog.date = body_data.get('date')
        classlog.time = body_data.get('time')
        classlog.gymclass_id = body_data.get('gymclass_id')
        classlog.trainer_id = body_data.get('trainer_id')
        classlog.member_id = body_data.get('member_id')

        # Add classlog to session
        db.session.add(classlog)
        # Commit classlog to session
        db.session.commit()
        # Respond to user
        return classlog_schema.dump(classlog), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'A classlog exists with overlapping details. Ensure trainers and members aren\'t double booking.'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required'}, 409



# Delete an entry to class log - auth required: trainers only
@classlog_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_trainer
def classlog_delete(id):
    # Look for classlog with id
    stmt = db.select(Classlog).filter_by(id=id)
    classlog = db.session.scalar(stmt)

    # If gymclass exists, delete classlog
    if classlog:
        db.session.delete(classlog)
        db.session.commit()
        return {'message': f'Classlog entry with id {id} removed successfully.'}
    else:
        return {'error': f'Classlog entry with id {id} does not exist.'}, 404


# Update an entry to class log - auth required: trainers only
@classlog_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_trainer
def classlog_update(id):
    try:
        # Obtain data from user input
        body_data = classlog_schema.load(request.get_json(), partial=True)
        
        # Look for classlog entry with id
        stmt = db.select(Classlog).filter_by(id=id)
        classlog = db.session.scalar(stmt)

        # Set up user input for conflict checking
        user_date = body_data.get('date') or classlog.date
        user_time = body_data.get('time') or classlog.time
        user_gymclassid = body_data.get('gymclass_id') or classlog.gymclass_id
        user_trainerid = body_data.get('trainer_id') or classlog.trainer_id

        # If classlog exists, update classlog
        if classlog:
            # Check if GymClass exists, if not return an error
            gymclass = GymClass.query.get(classlog.gymclass_id)
            if not gymclass:
                return {'error': f'Gym class with id {classlog.gymclass_id} does not exist.'}, 404
        
            # Check for class capacity
            if gymclass.max_cap:
                current_cap = Classlog.query.filter_by(
                    gymclass_id=user_gymclassid,
                    date=user_date,
                    time=user_time
                ).count()
                if current_cap >= gymclass.max_cap:
                    return {'error': f'Gym class with id {user_gymclassid} on {user_date} at {user_time} is full. Please try a different class.'}, 400
            
            # Check if a trainer has a conflicting class on the same date and time
            if Classlog.query.filter(
                Classlog.gymclass_id != user_gymclassid,
                Classlog.trainer_id==user_trainerid,
                Classlog.date==user_date,
                Classlog.time==user_time
            ).first():
                return {'error': f'Trainer with id {user_trainerid} is already teaching another class on {user_date} at {user_time}.'}, 400

            classlog.date = body_data.get('date') or classlog.date
            classlog.time = body_data.get('time') or classlog.time
            classlog.gymclass_id = body_data.get('gymclass_id') or classlog.gymclass_id
            classlog.trainer_id = body_data.get('trainer_id') or classlog.trainer_id
            classlog.member_id = body_data.get('member_id') or classlog.member_id            

            # Commit classlog changes to session
            db.session.commit()
            # Respond to user
            return classlog_schema.dump(classlog)
        else:
            return {'error': f'Classlog entry with id {id} does not exist.'}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'A classlog exists with overlapping details. Ensure trainers and members aren\'t double booking.'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required'}, 409