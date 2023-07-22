from flask import Blueprint
from init import db, bcrypt
from models.trainers import Trainer
from models.members import Member

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print('Tables created')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped')

@db_commands.cli.command('seed')
def seed_db():
    # Create our trainers
    trainers = [
        Trainer(
            first_name = 'Sofia',
            last_name = 'McMillan',
            dob = '1961-09-18',
            phone = '0490778163',
            email = 'SofiaMcMillan@email.com',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            emergency_contact_name = 'Caitlin Swain',
            emergency_contact_phone = '0453698752',
            first_aid_officer = True
        ),
        Trainer(
            first_name = 'Eve',
            last_name = 'Bruntnell',
            dob = '1947-08-12',
            phone = '0449562025',
            email = 'EveBruntnell@email.com',
            password = bcrypt.generate_password_hash('trainer2pw').decode('utf-8'),
            emergency_contact_name = 'Aaron Bradfield',
            emergency_contact_phone = '0447636546',
            first_aid_officer = True
        ),
        Trainer(
            first_name = 'Indiana',
            last_name = 'Biraban',
            dob = '1965-01-25',
            phone = '0493237723',
            email = 'IndianaBiraban@email.com',
            password = bcrypt.generate_password_hash('trainer3pw').decode('utf-8'),
            emergency_contact_name = 'Annabelle McMaster',
            emergency_contact_phone = '0440216072',
            first_aid_officer = False
        )
    ]
    # Add trainers to the session
    db.session.add_all(trainers)

    # Create our members
    members = [
        Member(
            first_name = 'Isla',
            last_name = 'Clibborn',
            dob = '1991-06-29',
            phone = '0453660173',
            email = 'IslaClibborn@email.com',
            password = bcrypt.generate_password_hash('user1pw').decode('utf-8'),
            emergency_contact_name = 'Liam Lovely',
            emergency_contact_phone = '0490634820'
        ),
        Member(
            first_name = 'Molly',
            last_name = 'Bryant',
            dob = '1961-12-28',
            phone = '0483597267',
            email = 'MollyBryant@email.com',
            password = bcrypt.generate_password_hash('user1pw').decode('utf-8'),
            emergency_contact_name = 'Elijah Burley',
            emergency_contact_phone = '0461642376'
        )
    ]
    # Add members to the session
    db.session.add_all(members)
    db.session.commit()

    print('Tables seeded')