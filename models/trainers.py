from main import db

class Trainer(db.Model):
    __tablename__ = 'trainers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    emergency_contact_name = db.Column(db.String(), nullable=False)
    emergency_contact_phone = db.Column(db.String(), nullable=False)
    first_aid_officer = db.Column(db.Boolean(), nullable=False)
    active_staff = db.Column(db.Boolean(), nullable=False, default=True)
    classlogs = db.relationship('Classlog', back_populates='trainer_id', cascade='all, delete')