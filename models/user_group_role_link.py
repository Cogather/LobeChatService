from models import db


class User_Link(db.Model):
    __tablename__ = 't_lobechat_user_group_role_link'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    link_group_id = db.Column(db.String(255))
    link_role_id = db.Column(db.String(255))
    def __init__(self, user_name, link_group_id,link_role_id):
        self.user_name = user_name
        self.link_group_id = link_group_id
        self.link_role_id = link_role_id