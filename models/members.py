from init import db, ma

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    emergency_contact_name = db.Column(db.String(), nullable=False)
    emergency_contact_phone = db.Column(db.String(), nullable=False)
    active_member = db.Column(db.Boolean(), nullable=False, default=True)
    classlogs = db.relationship('Classlog', back_populates='member_id', cascade='all, delete')