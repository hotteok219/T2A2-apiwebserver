from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db, bcrypt
from models.members import Member, member_schema, members_schema, memberpw_schema
from decorators.auth_decorator import authorise_as_trainer


member_bp = Blueprint('member', __name__, url_prefix='/member')


# Show list of members - auth required: trainers only
@member_bp.route('/')
@jwt_required()
@authorise_as_trainer
def member_list():
    stmt = db.select(Member)
    members = db.session.scalars(stmt)
    
    return members_schema.dump(members)


# Show specific member - auth required: trainers or a member can only view their own record
@member_bp.route('/<int:id>')
@jwt_required()
def member_list_one(id):
    # Look for member with id
    stmt = db.select(Member).filter_by(id=id)
    member = db.session.scalar(stmt)

    # If member exists, return member details
    if member:
        # Check if current user is a trainer or is a member with authorisation
        current_user = get_jwt_identity()
        if current_user.startswith('member') and str(member.id) != current_user[6:]:
            return {'error': 'You can only view your own details.'}, 403
        else:
            return member_schema.dump(member)
    # If member doesn't exist, return error
    else:
        return {'error': f'Member with id {id} does not exist.'}, 404            


# Delete a member - auth required: trainers only
@member_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_trainer
def member_delete(id):
    # Look for member with id
    stmt = db.select(Member).filter_by(id=id)
    member = db.session.scalar(stmt)

    # If member exists, delete member
    if member:
        db.session.delete(member)
        db.session.commit()
        return {'message': f'Member with id {id} removed successfully.'}
    else:
        return {'error': f'Member with id {id} does not exist.'}, 404


# Update a member - auth required: trainers or a member can only update their own record
@member_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def member_update(id):
    # Obtain data from user input - using memberpw_schema to enable password updates
    body_data = memberpw_schema.load(request.get_json(), partial=True)

    # Look for member with id
    stmt = db.select(Member).filter_by(id=id)
    member = db.session.scalar(stmt)

    # If member exists, update member
    if member:
        # Check if current user is a trainer or is a member with authorisation
        current_user = get_jwt_identity()
        if current_user.startswith('member') and str(member.id) != current_user[6:]:
            return {'error': 'You can only update your own details.'}, 403
        else:
            member.first_name = body_data.get('first_name') or member.first_name
            member.last_name = body_data.get('last_name') or member.last_name
            member.dob = body_data.get('dob') or member.dob
            member.phone = body_data.get('phone') or member.phone
            member.email =  body_data.get('email') or member.email
            member.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8') or member.password
            member.emergency_contact_name =  body_data.get('emergency_contact_name') or member.emergency_contact_name
            member.emergency_contact_phone = body_data.get('emergency_contact_phone') or member.emergency_contact_phone

            db.session.commit()
            # Respond to client without showing the password
            return member_schema.dump(member)
    # If member doesn't exist, return error
    else:
        return {'error': f'Member with id {id} does not exist.'}, 404