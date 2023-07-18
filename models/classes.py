from init import db, ma

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(), nullable=False)
    duration = db.Column(db.Float(), nullable=False)
    day = db.Column(db.String())
    time = db.Column(db.String())
    max_cap = db.Column(db.Integer())
    classlogs = db.relationship('Classlog', back_populates='class_id', cascade='all, delete')

class ClassSchema(db.Schema):
    class Meta:
        fields = ('id', 'class_name', 'duration', 'day', 'time', 'max_cap')

class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)