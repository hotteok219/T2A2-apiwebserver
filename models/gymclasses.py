from init import db

class GymClass(db.Model):
    __tablename__ = 'gymclasses'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    day = db.Column(db.String())
    time = db.Column(db.Time)
    max_cap = db.Column(db.Integer())
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)

    trainer = db.relationship('Trainer', back_populates='gymclasses')
    classlog = db.relationship('Classlog', back_populates='gymclasses')
    
    # Creating unique constraints to prevent duplication
    __table_args__ = (
        db.UniqueConstraint('class_name', 'day', 'time'),
        db.UniqueConstraint('trainer_id', 'day', 'time'),
    )