from init import db, ma

class Classlog(db.Model):
    __tablename__ = 'classlogs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    gymclass_id = db.Column(db.Integer, db.ForeignKey('gymclasses.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))

    gymclasses = db.relationship('GymClass', back_populates='classlog')
    member = db.relationship('Member', back_populates='classlog')
    trainer = db.relationship('Trainer', back_populates='classlog')

class ClasslogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'gymclass_id', 'trainer_id', 'member_id')
        ordered = True

classlog_schema = ClasslogSchema()
classlogs_schema = ClasslogSchema(many=True)