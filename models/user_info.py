from models import db

class User_Info(db.Model):
    __tablename__ = 't_lobechat_user_info'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    chn_name = db.Column(db.String(255))
    departmentL1 = db.Column(db.String(255))
    departmentL2 = db.Column(db.String(255))
    departmentL3 = db.Column(db.String(255))
    departmentL4 = db.Column(db.String(255))
    departmentL5 = db.Column(db.String(255))
    departmentL6 = db.Column(db.String(255))

    def __init__(self, user_name, chn_name, departmentL1, departmentL2, departmentL3, departmentL4,
                     departmentL5, departmentL6):
        self.user_name = user_name
        self.chn_name = chn_name
        self.departmentL1 = departmentL1
        self.departmentL2 = departmentL2
        self.departmentL3 = departmentL3
        self.departmentL4 = departmentL4
        self.departmentL5 = departmentL5
        self.departmentL6 = departmentL6