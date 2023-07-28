from marshmallow import fields
from marshmallow.validate import Length
from init import ma


class GymClassSchema(ma.Schema):
    trainer = fields.Nested('TrainerSchema', only=['first_name', 'last_name'])

    class_name = fields.String(validate=Length(min=2, error='Class name must be at least 2 characters long.'))

    class Meta:
        fields = ('id', 'class_name', 'duration', 'day', 'time', 'max_cap', 'trainer_id', 'trainer')
        ordered = True

gymclass_schema = GymClassSchema()
gymclasses_schema = GymClassSchema(many=True)