from init import db, ma
from marshmallow import fields

class Trainer(db.Model):
    __tablename__ = 'trainers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    emergency_contact_name = db.Column(db.String(), nullable=False)
    emergency_contact_phone = db.Column(db.String(), nullable=False)
    first_aid_officer = db.Column(db.Boolean(), default=False)
    # classlogs = db.relationship('Classlog', back_populates='trainer_id', cascade='all, delete')

class TrainerSchema(ma.Schema):
#     classlogs = fields.List(fields.Nested('ClasslogSchema', exclude=['user_id']))

    class Meta:
        fields = ( 'id', 'first_name', 'last_name', 'dob', 'phone', 'email', 'password', 'emergency_contact_name', 'emergency_contact_phone', 'first_aid_officer')

trainer_schema = TrainerSchema(exclude=['password'])
trainers_schema = TrainerSchema(many=True, exclude=['password'])
trainerpw_schema = TrainerSchema()