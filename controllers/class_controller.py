from flask import Blueprint, request


class_bp = Blueprint('class', __name__, url_prefix='/class')


# Show list of classes - no auth required
@class_bp.route('/')
def class_list():
    pass



# Show specific class - no auth required
@class_bp.route('/<int:id>')
def class_id():
    pass



# Register a class - auth required: trainers only
@class_bp.route('/', methods=['POST'])
def class_register():
    pass



# Delete a class - auth required: trainers only
@class_bp.route('/<int:id>', methods=['DELETE'])
def class_delete():
    pass



# Update a class - auth required: trainers only
@class_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def class_update():
    pass