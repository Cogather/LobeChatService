from models import db


class Notices(db.Model):
    __tablename__ = 'lobechat_notices_records'

    id = db.Column(db.Integer, primary_key=True)
    notice = db.Column(db.String(255))
    creator = db.Column(db.String(255))
    start_time = db.Column(db.String(100))
    expected_end_time = db.Column(db.String(100))
    expiration_time = db.Column(db.Integer)
    is_valid = db.Column(db.Integer)
    platform_id = db.Column(db.Integer)
    type = db.Column(db.Integer)


    def __init__(self, notice, creator, start_time,expiration_time,expected_end_time,is_valid,platform_id,type):
        self.notice = notice
        self.creator = creator
        self.start_time = start_time
        self.expiration_time = expiration_time
        self.expected_end_time = expected_end_time
        self.is_valid = is_valid
        self.platform_id = platform_id
        self.type = type