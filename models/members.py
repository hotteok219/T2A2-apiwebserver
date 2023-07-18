from init import db, ma

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    emergency_contact_name = db.Column(db.String(), nullable=False)
    emergency_contact_phone = db.Column(db.String(), nullable=False)
    active_member = db.Column(db.Boolean(), default=True)
    # classlogs = db.relationship('Classlog', back_populates='member_id', cascade='all, delete')
    
class MemberSchema(ma.Schema):
    class Meta:
        fields = ( 'id', 'first_name', 'last_name', 'dob', 'phone', 'email', 'password', 'emergency_contact_name ', 'emergency_contact_phone', 'active_member')

member_schema = MemberSchema(exclude=['password'])
members_schema = MemberSchema(many=True, exclude=['password'])