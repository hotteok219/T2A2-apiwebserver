from flask import Blueprint
from init import db, bcrypt
from models.trainers import Trainer
from models.members import Member
from models.gymclasses import GymClass
from models.classlogs import Classlog

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
            email = 'SofiaMcMillan@email.com'.lower(),
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
            email = 'EveBruntnell@email.com'.lower(),
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
            email = 'IndianaBiraban@email.com'.lower(),
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
			first_name = 'Fred',
			last_name = 'Flintstone',
			dob = '1960-04-01',
			phone = '0453660184',
			email = 'FredFlintstone@email.com'.lower(),
			password = bcrypt.generate_password_hash('user1pw').decode('utf-8'),
			emergency_contact_name = 'Wilma Flintstone',
			emergency_contact_phone = '0490634831'
		),
		Member(
			first_name = 'Mickey',
			last_name = 'Mouse',
			dob = '1928-11-18',
			phone = '0453660174',
			email = 'MickeyMouse@email.com'.lower(),
			password = bcrypt.generate_password_hash('user2pw').decode('utf-8'),
			emergency_contact_name = 'Minnie Mouse',
			emergency_contact_phone = '0490634821'
		),
		Member(
			first_name = 'Donald',
			last_name = 'Duck',
			dob = '1934-06-09',
			phone = '0453660175',
			email = 'DonaldDuck@email.com'.lower(),
			password = bcrypt.generate_password_hash('user3pw').decode('utf-8'),
			emergency_contact_name = 'Daisy Duck',
			emergency_contact_phone = '0490634822'
		),
		Member(
			first_name = 'Bugs',
			last_name = 'Bunny',
			dob = '1940-07-27',
			phone = '0453660176',
			email = 'BugsBunny@email.com'.lower(),
			password = bcrypt.generate_password_hash('user4pw').decode('utf-8'),
			emergency_contact_name = 'Lola Bunny',
			emergency_contact_phone = '0490634823'
		),
		Member(
			first_name = 'Scooby',
			last_name = 'Doo',
			dob = '1969-09-13',
			phone = '0453660177',
			email = 'ScoobyDoo@email.com'.lower(),
			password = bcrypt.generate_password_hash('user5pw').decode('utf-8'),
			emergency_contact_name = 'Shaggy Rogers',
			emergency_contact_phone = '0490634824'
		),
		Member(
			first_name = 'Homer',
			last_name = 'Simpson',
			dob = '1956-05-12',
			phone = '0453660178',
			email = 'HomerSimpson@email.com'.lower(),
			password = bcrypt.generate_password_hash('user6pw').decode('utf-8'),
			emergency_contact_name = 'Marge Simpson',
			emergency_contact_phone = '0490634825'
		),
		Member(
			first_name = 'Bart',
			last_name = 'Simpson',
			dob = '1980-04-01',
			phone = '0453660179',
			email = 'BartSimpson@email.com'.lower(),
			password = bcrypt.generate_password_hash('user7pw').decode('utf-8'),
			emergency_contact_name = 'Lisa Simpson',
			emergency_contact_phone = '0490634826'
		),
		Member(
			first_name = 'SpongeBob',
			last_name = 'SquarePants',
			dob = '1999-05-01',
			phone = '0453660180',
			email = 'SpongeBobSquarePants@email.com'.lower(),
			password = bcrypt.generate_password_hash('user8pw').decode('utf-8'),
			emergency_contact_name = 'Patrick Star',
			emergency_contact_phone = '0490634827'
		),
		Member(
			first_name = 'Scooby',
			last_name = 'Doo',
			dob = '1969-09-13',
			phone = '0453660181',
			email = 'ScoobyDoo1@email.com'.lower(),
			password = bcrypt.generate_password_hash('user9pw').decode('utf-8'),
			emergency_contact_name = 'Shaggy Rogers',
			emergency_contact_phone = '0490634828'
		),
		Member(
			first_name = 'Blossom',
			last_name = 'Utonium',
			dob = '1992-04-01',
			phone = '0453660182',
			email = 'BlossomUtonium@email.com'.lower(),
			password = bcrypt.generate_password_hash('user10pw').decode('utf-8'),
			emergency_contact_name = 'Professor Utonium',
			emergency_contact_phone = '0490634829'
		)
    ]
    # Add members to the session
    db.session.add_all(members)

    # Create our gym classes
    gymclasses = [
        GymClass (
            class_name = 'Pilates',
            duration = '60',
            day = 'Monday',
            time = '6:00 pm',
            max_cap = '12',
            trainer = trainers[2]
        ),
        GymClass (
            class_name = 'Boxing',
            duration = '45',
            day = 'Wednesday',
            time = '5:45 pm',
            max_cap = '10',
            trainer = trainers[1]
        ),
        GymClass (
            class_name = 'Zumba',
            duration = '60',
            day = 'Friday',
            time = '7:00 pm',
            max_cap = '12',
            trainer = trainers[2]
        )
    ]
    # Add gym classes to the session
    db.session.add_all(gymclasses)

    # Create classlog
    classlogs = [
        Classlog (
            date = '2023-07-03',
            time = '6:00 pm',
            gymclass_id = '1',
            trainer_id = '2',
            member_id = '1'
        ),
        Classlog (
            date = '2023-07-03',
            time = '6:00 pm',
            gymclass_id = '1',
            trainer_id = '2',
            member_id = '2'
        ),
        Classlog (
            date = '2023-07-03',
            time = '6:00 pm',
            gymclass_id = '1',
            trainer_id = '2',
            member_id = '3'
        ),
        Classlog (
            date = '2023-07-05',
            time = '5:45 pm',
            gymclass_id = '2',
            trainer_id = '2',
            member_id = '1'
        ),
        Classlog (
            date = '2023-07-05',
            time = '5:45 pm',
            gymclass_id = '2',
            trainer_id = '2',
            member_id = '2'
        ),
        Classlog (
            date = '2023-07-05',
            time = '5:45 pm',
            gymclass_id = '2',
            trainer_id = '2',
            member_id = '3'
        ),
        Classlog (
            date = '2023-07-05',
            time = '5:45 pm',
            gymclass_id = '2',
            trainer_id = '2',
            member_id = '4'
        ),
        Classlog (
            date = '2023-07-05',
            time = '5:45 pm',
            gymclass_id = '2',
            trainer_id = '2',
            member_id = '5'
        )
    ]
    # Add class logs to the session
    db.session.add_all(classlogs)

    # Commit all
    db.session.commit()

    print('Tables seeded')