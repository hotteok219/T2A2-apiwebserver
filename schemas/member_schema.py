from marshmallow import fields
from marshmallow.validate import Email, Regexp, Length
from init import ma


class MemberSchema(ma.Schema):
    first_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Only letters, spaces and hyphens are allowed'))
    last_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Only letters, spaces and hyphens are allowed'))
    phone = fields.String(required=True, validate=Regexp('^[0-9 ]+$', error='Only numbers and spaces are allowed'))
    email = fields.String(validate=Email(error='Enter a valid email address.'))
    password = fields.String(validate=Length(min=6, error='Password should be at least 6 characters.'))
    emergency_contact_name = fields.String(required=True, validate=Regexp('^[a-zA-Z -]+$', error='Only letters, spaces and hyphens are allowed'))
    emergency_contact_phone = fields.String(required=True, validate=Regexp('^[0-9 ]+$', error='Only numbers and spaces are allowed'))

    class Meta:
        fields = ( 'id', 'first_name', 'last_name', 'dob', 'phone', 'email', 'password', 'emergency_contact_name ', 'emergency_contact_phone')
        ordered = True

member_schema = MemberSchema(exclude=['password'])
members_schema = MemberSchema(many=True, exclude=['password'])
memberpw_schema = MemberSchema()