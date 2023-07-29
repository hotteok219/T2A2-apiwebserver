from init import db

class Classlog(db.Model):
    __tablename__ = 'classlogs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    gymclass_id = db.Column(db.Integer, db.ForeignKey('gymclasses.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)

    gymclasses = db.relationship('GymClass', back_populates='classlog')
    member = db.relationship('Member', back_populates='classlog')
    trainer = db.relationship('Trainer', back_populates='classlog')
    
    # Creating unique constraints to prevent duplication
    __table_args__ = (
        db.UniqueConstraint('date', 'time', 'gymclass_id', 'trainer_id', 'member_id'),
        db.UniqueConstraint('date', 'time', 'member_id'),
    )