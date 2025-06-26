from models import db


class UserAccessInfo(db.Model):
    __tablename__ = 'user_access_data'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    access_time = db.Column(db.String(100))
    access_platform  = db.Column(db.String(20))

    def __init__(self, user_name, access_time, access_platform):
        self.user_name = user_name
        self.access_time = access_time
        self.access_platform = access_platform