
from models import db


class FavoritesRecords(db.Model):
    __tablename__ = 'user_favorites_records'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    tool_id = db.Column(db.Integer)
    is_add = db.Column(db.String(255))
    def __init__(self, user_name, tool_id,is_add):
        self.user_name = user_name
        self.tool_id = tool_id
        self.is_add = is_add