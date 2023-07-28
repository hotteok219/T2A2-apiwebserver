from init import db


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
