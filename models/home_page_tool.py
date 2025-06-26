
from models import db


class HomePageTool(db.Model):
    __tablename__ = 'home_page_tool_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category_id = db.Column(db.Integer)
    category_name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    url = db.Column(db.String(255))
    favorites = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    icon_url = db.Column(db.String(255))
    tags = db.Column(db.String(255))

    def __init__(self, name, category_id, category_name, description, url,favorites,image_url,tags,icon_url):
        self.name = name
        self.category_id = category_id
        self.category_name = category_name
        self.description = description
        self.url = url
        self.favorites = favorites
        self.image_url = image_url
        self.tags = tags
        self.icon_url = icon_url

# 添加一个方法来将对象转换为字典
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'description': self.description,
            'url': self.url,
            'favorites': self.favorites,
            'image': self.image_url,
            'tags': self.tags,
            'icon': self.icon_url
        }