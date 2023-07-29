from marshmallow import fields
from marshmallow.validate import Length, OneOf
from init import ma

VALID_DAYS = (
    'Monday', 
    'Tuesday', 
    'Wednesday', 
    'Thursday', 
    'Friday', 
    'Saturday', 
    'Sunday'
)

class GymClassSchema(ma.Schema):
    trainer = fields.Nested('TrainerSchema', only=['first_name', 'last_name'])

    class_name = fields.String(validate=Length(min=2, error='Class name must be at least 2 characters long.'))
    duration = fields.Integer()
    day = fields.String(validate=OneOf(VALID_DAYS))
    time = fields.Time(format='%I:%M %p', error_messages={'invalid': 'Please ensure the time is in the format HH:MM AM/PM'})
    max_cap = fields.Integer()
    trainer_id = fields.Integer()

    class Meta:
        fields = ('id', 'class_name', 'duration', 'day', 'time', 'max_cap', 'trainer_id', 'trainer')
        ordered = True


gymclass_schema = GymClassSchema()
gymclasses_schema = GymClassSchema(many=True)