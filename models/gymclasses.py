from marshmallow import fields
from init import db, ma

class GymClass(db.Model):
    __tablename__ = 'gymclasses'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(), nullable=False)
    duration = db.Column(db.String(), nullable=False)
    day = db.Column(db.String())
    time = db.Column(db.String())
    max_cap = db.Column(db.Integer())
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)

    trainer = db.relationship('Trainer', back_populates='gymclasses')
    classlog = db.relationship('Classlog', back_populates='gymclasses')

class GymClassSchema(ma.Schema):
    trainer = fields.Nested('TrainerSchema', only=['first_name', 'last_name'])

    class Meta:
        fields = ('id', 'class_name', 'duration', 'day', 'time', 'max_cap', 'trainer_id', 'trainer')
        ordered = True

gymclass_schema = GymClassSchema()
gymclasses_schema = GymClassSchema(many=True)