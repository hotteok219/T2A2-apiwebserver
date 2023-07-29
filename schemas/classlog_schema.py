from marshmallow import fields
from init import ma

class ClasslogSchema(ma.Schema):
    date = fields.Date()
    time = fields.Time(format='%I:%M %p', error_messages={'invalid': 'Please ensure the time is in the format HH:MM AM/PM'})
    gymclass_id = fields.Integer()
    trainer_id = fields.Integer()
    member_id = fields.Integer()

    class Meta:
        fields = ('id', 'date', 'time', 'gymclass_id', 'trainer_id', 'member_id')
        ordered = True


classlog_schema = ClasslogSchema()
classlogs_schema = ClasslogSchema(many=True)