
from models import db


class UserFavoritesData(db.Model):
    __tablename__ = 'user_favorites_data'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    tool_id = db.Column(db.Integer)
    def __init__(self, user_name, tool_id):
        self.user_name = user_name
        self.tool_id = tool_id