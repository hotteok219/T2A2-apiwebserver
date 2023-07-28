from marshmallow import fields
from marshmallow.validate import Regexp, Email, Length
from init import ma


class TrainerSchema(ma.Schema):
    first_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Only letters, spaces and hyphens are allowed'))
    last_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Only letters, spaces and hyphens are allowed'))
    phone = fields.String(required=True, validate=Regexp('^[0-9 ]+$', error='Only numbers and spaces are allowed'))
    email = fields.Email(validate=Email(error='Enter a valid email address.'))
    password = fields.String(validate=Length(min=6, error='Password should be at least 6 characters.'))
    emergency_contact_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Only letters, spaces and hyphens are allowed'))
    emergency_contact_phone = fields.String(required=True, validate=Regexp('^[0-9 ]+$', error='Only numbers and spaces are allowed'))
    # first_aid_officer = fields.Boolean(error='Enter True or False.')
    
    gymclasses = fields.List(fields.Nested('GymClassSchema', only=['class_name']))

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'dob', 'phone', 'email', 'password', 'emergency_contact_name', 'emergency_contact_phone', 'first_aid_officer', 'gymclasses')
        ordered = True


trainer_schema = TrainerSchema(exclude=['password'])
trainers_schema = TrainerSchema(many=True, exclude=['password'])
trainerpw_schema = TrainerSchema()