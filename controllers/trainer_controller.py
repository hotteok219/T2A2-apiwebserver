from flask import Blueprint, request
from init import db, bcrypt
from models.trainers import Trainer, trainer_schema, trainers_schema
from models.members import Member, member_schema, members_schema

trainer_bp = Blueprint('trainer', __name__, url_prefix='/trainer')

@trainer_bp.route('/register', methods=['POST'])
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