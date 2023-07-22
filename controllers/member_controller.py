from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from datetime import timedelta
import functools
from init import db, bcrypt
from models.members import Member, member_schema, members_schema, memberpw_schema
from models.trainers import Trainer


member_bp = Blueprint('member', __name__, url_prefix='/member')



# Limit authority to trainer
def authorise_as_trainer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        trainer_id = get_jwt_identity()
        stmt = db.select(Trainer).filter_by(id=trainer_id)
        trainer = db.session.scalar(stmt)
        print(trainer)
        if trainer:
            return fn(*args, **kwargs)
        else:
            return {'error': 'You are not authorised to perform this transaction.'}, 403
    return wrapper



# Show list of members - auth required: trainers only
@member_bp.route('/')
@jwt_required()
@authorise_as_trainer
def member_list():
    stmt = db.select(Member)
    members = db.session.scalars(stmt)
    
    return members_schema.dump(members)



# Show specific member - auth required: trainers only
@member_bp.route('/<int:id>')
@jwt_required()
@authorise_as_trainer
def member_id(id):
    # Look for member with id
    stmt = db.select(Member).filter_by(id=id)
    member = db.session.scalar(stmt)

    # If member exists, return member details
    if member:
        return member_schema.dump(member)
    # If member doesn't exist, return error
    else:
        return {'error': f'Member with id {id} does not exist.'}, 404



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
        # Set an expiry on the token
        token = create_access_token(identity=str(member.id), expires_delta=timedelta(days=1))
        return {'email': member.email, 'token': token}
    # If member doesn't exist, return error
    else:
        return {'error': 'Invalid email or password.'}, 401



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
@authorise_as_trainer
def member_update(id):
    # Obtain data from user input - using memberpw_schema to enable password updates
    body_data = memberpw_schema.load(request.get_json(), partial=True)

    # Look for member with id
    stmt = db.select(Member).filter_by(id=id)
    member = db.session.scalar(stmt)

    # If member exists, update member
    if member:
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
    else:
        return {'error': f'Member with id {id} does not exist.'}, 404