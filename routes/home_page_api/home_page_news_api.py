import json
import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy import text

from models import db
from models.news_catalog import Catalog
from models.news_data import NewsData

news_api_bp = Blueprint('news_api', __name__)

@news_api_bp.route('/get_catalog_list', methods=['GET'])
def get_catalog_list():
    try:
        # 按照时间降序排序
        catalog_list = Catalog.query.order_by(text("STR_TO_DATE(value, '%Y.%m.%d') DESC")).all()
        result_list = []
        # 对象转字典，返给用户
        for catalog in catalog_list:
            result_list.append(catalog.to_dict())
        return result_list
    except Exception as e:
        traceback.print_exc()  # 打印完整堆栈（包括源代码行号）
        return jsonify({"error":"查询资讯目录出错！！"}),500
    finally:
        db.session.close()

# 根据目录id 查询当前资讯详情
@news_api_bp.route('/get_news_list/<catalog_id>', methods=['GET'])
def get_news_list(catalog_id):
    try:
        news_data = NewsData.query.filter(NewsData.catalog_id == catalog_id).first()
        # 对象转字典
        news_data_dict = news_data.to_dict()
        return news_data_dict
    except Exception as e:
        traceback.print_exc()  # 打印完整堆栈（包括源代码行号）
        return jsonify({"error":"查询资讯数据出错！！"}),500
    finally:
        db.session.close()

# 新增资讯目录
@news_api_bp.route('/add_news_catalog', methods=['POST'])
def add_news_catalog():
    catalog_list = []
    data_list = request.get_json()
    for data in data_list:
        value = data.get("value")
        label = data.get("label")
        title = data.get("title")
        catalog = Catalog(value=value, label=label, title=title)
        catalog_list.append(catalog)
    try:
        db.session.add_all(catalog_list)
        db.session.commit()
        return jsonify({"message":"资讯目录新增成功"})
    except Exception as e:
        traceback.print_exc()  # 打印完整堆栈（包括源代码行号）
        return jsonify({"error":"新增资讯目录出错！！"}),500
    finally:
        db.session.close()

# 新增资讯数据
@news_api_bp.route('/add_news', methods=['POST'])
def add_news():
    new_datas = request.get_json()
    news_data_list = []
    for data in new_datas:
        value = data.get("value")
        section_data_list = data.get("sectionData")
        another_data_list = data.get("anotherData")
        # 如果是字典，将其转为JSON字符串
        if isinstance(section_data_list, dict):
            section_data_text = json.dumps(section_data_list, ensure_ascii=False)
        elif section_data_list is None:
            section_data_text = ""
        else:
            section_data_text = str(section_data_list)

        if isinstance(another_data_list, dict):
            another_data_text = json.dumps(another_data_list, ensure_ascii=False)
        elif another_data_list is None:
            another_data_text = ""
        else:
            another_data_text = str(another_data_list)

        # 根据value查询日志id
        catalog_id = Catalog.query.filter(Catalog.value == value).first().catalog_id
        news_data = NewsData(catalog_id=catalog_id, value=value, sectionData=section_data_text, anotherData=another_data_text)
        news_data_list.append(news_data)
    try:
        db.session.add_all(news_data_list)
        db.session.commit()
        return jsonify({"message":"资讯数据新增成功"})
    except Exception as e:
        traceback.print_exc()  # 打印完整堆栈（包括源代码行号）
        return jsonify({"error":"新增资讯数据出错！！"}),500
    finally:
        db.session.close()
