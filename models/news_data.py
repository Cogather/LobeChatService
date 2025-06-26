import ast
import json

from models import db

# 其他资讯对象
class NewsData(db.Model):
    __tablename__ = 'news_section_data'

    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255))
    catalog_id = db.Column(db.Integer)
    sectionData = db.Column(db.Text)
    anotherData = db.Column(db.Text)

    def __init__(self, value, catalog_id,sectionData,anotherData):
        self.value = value
        self.catalog_id = catalog_id
        self.sectionData = sectionData
        self.anotherData = anotherData


    def to_dict(self):
        def text_to_data(text):
            try:
                # 尝试用json.loads（处理标准JSON）
                return json.loads(text)
            except Exception:
                # 如果是python字面值（单引号风格）
                return ast.literal_eval(text)
        return {
            'value': self.value,
            'sectionData': text_to_data(self.sectionData),  # 转换Text到JSON
            'anotherData': text_to_data(self.anotherData)  # 同上
        }

