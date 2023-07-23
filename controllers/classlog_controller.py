from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from init import db
from models.classlogs import Classlog, classlog_schema, classlogs_schema
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
    # Obtain data from user input
    body_data = request.get_json()

    # Create a new instance of the Classlog model
    classlog = Classlog()
    classlog.date = body_data.get('date')
    classlog.gymclass_id = body_data.get('gymclass_id')
    classlog.trainer_id = body_data.get('trainer_id')
    classlog.member_id = body_data.get('member_id')

    # Add classlog to session
    db.session.add(classlog)
    # Commit classlog to session
    db.session.commit()
    # Respond to user
    return classlog_schema.dump(classlog), 201


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
    # Obtain data from user input
    body_data = classlog_schema.load(request.get_json(), partial=True)

    # Look for classlog entry with id
    stmt = db.select(Classlog).filter_by(id=id)
    classlog = db.session.scalar(stmt)

    # If classlog exists, update classlog
    if classlog:
        classlog.date = body_data.get('date') or classlog.date
        classlog.gymclass_id = body_data.get('gymclass_id') or classlog.gymclass_id
        classlog.trainer_id = body_data.get('trainer_id') or classlog.trainer_id
        classlog.member_id = body_data.get('member_id') or classlog.member_id

        # Commit classlog changes to session
        db.session.commit()
        # Respond to user
        return classlog_schema.dump(classlog)
    else:
        return {'error': f'Classlog entry with id {id} does not exist.'}, 404