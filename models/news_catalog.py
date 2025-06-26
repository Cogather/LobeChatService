from models import db

# 资讯目录对象
class Catalog(db.Model):
    __tablename__ = 'news_catalog_data'

    catalog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255))
    label = db.Column(db.String(255))
    title = db.Column(db.String(255))

    def __init__(self, value, label, title):
        self.value = value
        self.label = label
        self.title = title

        # 添加一个方法来将对象转换为字典
    def to_dict(self):
        return {
            'catalog_id':self.catalog_id,
            'value': self.value,
            'label': self.label,
            'title': self.title
        }

