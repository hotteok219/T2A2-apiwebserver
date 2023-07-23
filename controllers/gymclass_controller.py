from flask import Blueprint, request
from init import db
from models.classes import GymClassSchema, gymclass_schema, gymclasses_schema


gymclass_bp = Blueprint('gymclass', __name__, url_prefix='/class')


# Show list of classes - no auth required
@gymclass_bp.route('/')
def gymclass_list():
    stmt = db.select(Class)
    classes = db.session.scalars(stmt)

    return classes_schema.dump(classes)


# Show specific class - no auth required
@gymclass_bp.route('/<int:id>')
def gymclass_id(id):
    pass



# Register a class - auth required: trainers only
@gymclass_bp.route('/', methods=['POST'])
def gymclass_register():
    pass



# Delete a class - auth required: trainers only
@gymclass_bp.route('/<int:id>', methods=['DELETE'])
def gymclass_delete():
    pass



# Update a class - auth required: trainers only
@gymclass_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def gymclass_update():
    pass