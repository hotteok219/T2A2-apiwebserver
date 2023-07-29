from marshmallow import fields, validates
from marshmallow.validate import Regexp, Length
from init import ma
from decorators.val_decorator import validate_name, validate_number

class TrainerSchema(ma.Schema):
    first_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='First name must be at least 1 character. Only letters, spaces and hyphens are allowed'))
    last_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Last name must be at least 1 character. Only letters, spaces and hyphens are allowed'))
    dob = fields.Date()
    phone = fields.String(required=True, validate=Regexp('^[0-9 ]+$', error='Only numbers and spaces are allowed'))
    email = fields.Email()
    password = fields.String(validate=Length(min=6, error='Password should be at least 6 characters.'))
    emergency_contact_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Only letters, spaces and hyphens are allowed'))
    emergency_contact_phone = fields.String(required=True, validate=Regexp('^[0-9 ]+$', error='Only numbers and spaces are allowed'))
    first_aid_officer = fields.Boolean()
    
    gymclasses = fields.List(fields.Nested('GymClassSchema', only=['class_name']))

    @validates('first_name')
    def validate_first_name(self, value):
        return validate_name(value, 'First name')
    
    @validates('last_name')
    def validate_last_name(self, value):
        return validate_name(value, 'Last name')
    
    @validates('phone')
    def validate_phone(self, value):
        return validate_number(value, 'Phone number')
    
    @validates('emergency_contact_name')
    def validate_emergency_contact_name(self, value):
        return validate_name(value, 'Emergency contact name')
    
    @validates('emergency_contact_phone')
    def validate_emergency_contact_phone(self, value):
        return validate_number(value, 'Emergency contact phone number')

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'dob', 'phone', 'email', 'password', 'emergency_contact_name', 'emergency_contact_phone', 'first_aid_officer', 'gymclasses')
        ordered = True


trainer_schema = TrainerSchema(exclude=['password'])
trainers_schema = TrainerSchema(many=True, exclude=['password'])
trainerpw_schema = TrainerSchema()