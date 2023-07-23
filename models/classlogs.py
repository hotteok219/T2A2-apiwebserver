from init import db, ma

class Classlog(db.Model):
    __tablename__ = 'classlogs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)

class ClasslogSchema(db.Schema):
    class Meta:
        fields = ('id', 'date', 'class_id', 'member_id', 'trainer_id')

classlog_schema = ClasslogSchema()
classlogs_schema = ClasslogSchema(many=True)