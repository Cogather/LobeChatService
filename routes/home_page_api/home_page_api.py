import json
from flask import Blueprint, request, jsonify
from sqlalchemy import update

from config_cache import cache
from models import db
from models.home_page_tool import HomePageTool
from models.message import Message
from models.token_balance import TokenBalance
from models.user_favorites_data import UserFavoritesData
from models.user_favorites_records import FavoritesRecords
from models.user_info import User_Info

home_page_api_bp = Blueprint('home_page_api', __name__)

@home_page_api_bp.route('/get_tool_list', methods=['GET'])
def get_tool_list():
    # 1. 定义缓存 key）
    cache_key = 'get_tool_list'
    # 2. 查看是否已缓存
    cached_result = cache.get(cache_key)
    if cached_result:
        print("缓存数据")
        return json.dumps(cached_result, ensure_ascii=False)
    tool_list = HomePageTool.query.all()
        # 将每个对象转换为字典，并使用 json.dumps 序列化
    tool_list_as_dicts = [tool.to_dict() for tool in tool_list]
    # 设置缓存
    cache.set(cache_key, tool_list_as_dicts, timeout=86400)
    return json.dumps(tool_list_as_dicts, ensure_ascii=False)

@home_page_api_bp.route('/update_tool', methods=['PUT'])
def update_tool():
    data = request.get_json()
    old_home_page_tool = HomePageTool.query.filter_by(id=data.get("id")).first()
    if not old_home_page_tool:
        return jsonify({"error": "Product not found"}), 404
    try:
        stmt = (
            update(HomePageTool)
            .where(HomePageTool.id == data.get('id'))
            .values(**data)
        )
        db.session.execute(stmt)
        db.session.commit()
        if cache.get("get_tool_list"):
            cache.delete('get_tool_list')
        return jsonify({"message": "修改成功"})
    except Exception as e:
        return jsonify({"message": "操作失败"})

@home_page_api_bp.route('/add_tool', methods=['POST'])
def add_tool():
    data = request.get_json()
    try:
        home_page_tool = HomePageTool(name=data.get("name"),category_id=data.get("category_id"),category_name=data.get("category_name"),
                                          description=data.get("description"),url=data.get("url"),favorites=data.get("favorites"),
                                          image_url=data.get("image_url"),icon_url=data.get("icon_url"),tags=data.get("tags"))
        db.session.add(home_page_tool)
        db.session.commit()
        if cache.get("get_tool_list"):
            cache.delete('get_tool_list')
        return jsonify({"message": "添加成功"})
    except Exception as e:
        print(e)
        return jsonify({"message": "添加失败"})

@home_page_api_bp.route('/remove_tool/<int:tool_id>', methods=['DELETE'])
def remove_tool(tool_id):
    try:
        # 直接根据id删除，返回受影响的行数
        rows_deleted = db.session.query(HomePageTool).filter(HomePageTool.id == tool_id).delete()
        db.session.commit()

        if rows_deleted == 0:
            return jsonify({"message": "工具不存在", "code": 404})

        # 清理缓存
        if cache.get("get_tool_list"):
            cache.delete('get_tool_list')
        return jsonify({"message": "删除成功", "code": 200})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "删除失败", "code": 500})

@home_page_api_bp.route('/get_by_id/<int:tool_id>', methods=['GET'])
def get_update_tool(tool_id):
    try:
    # 修改回显
        home_page_tool = HomePageTool.query.filter_by(id=tool_id).first()
        if home_page_tool:
            return jsonify(home_page_tool.to_dict)
    except Exception as e:
        print(e)
        return jsonify({"message": "操作失败"})
    else:
        return jsonify({"message": "未找到该工具"})

# 用户点击收藏或者取消收藏接口
@home_page_api_bp.route('/favorites', methods=['POST'])
def home_page_favorites():
    json_data = request.get_json()
    is_favorites = json_data.get('is_favorites')
    tool_id = json_data.get('tool_id')
    user_name = json_data.get('user_name')
    try:
        if is_favorites is True:
            # 用户点击收藏
            HomePageTool.query.filter_by(id=tool_id).update({HomePageTool.favorites: HomePageTool.favorites + 1})
            user_favorites_data = UserFavoritesData(user_name=user_name,tool_id=tool_id)
            db.session.add(user_favorites_data)
            favorites_records = FavoritesRecords(user_name=user_name,tool_id=tool_id,is_add = "1")
            db.session.add(favorites_records)
        else:
            # 用户取消收藏
            HomePageTool.query.filter_by(id=tool_id).update({HomePageTool.favorites: HomePageTool.favorites - 1})
            UserFavoritesData.query.filter_by(user_name=user_name, tool_id=tool_id).delete()
            favorites_records = FavoritesRecords(user_name=user_name,tool_id=tool_id,is_add = "0")
            db.session.add(favorites_records)
        # 新增或者删除失败后，需要删除缓存
        if cache.get("get_tool_list"):
            cache.delete('get_tool_list')
        db.session.commit()
        return jsonify({"code": 200, "message": "操作成功"})
    except Exception as e:
        # 插入异常，回滚
        db.session.rollback()
        print("报错信息：{}".format(e))
        return jsonify({"code": 500, "message": "操作失败"})

# 首页用户信息
@home_page_api_bp.route('/<string:user_name>', methods=['GET'])
def home_page_personal_center(user_name):
    # joined = db.session.query(表a, 表b).join(表b, 表a.tool_id == 表b.tool_id).filter(表a.工号 == '1001')
    joined = (db.session.query(UserFavoritesData, HomePageTool)
              .join(HomePageTool, UserFavoritesData.tool_id == HomePageTool.id)
              .filter(UserFavoritesData.user_name == user_name))
    # 将结果转换为字典列表
    result_list = []
    for user_favorites, home_page_tool in joined:
        result_dict = {
            "user_name": user_favorites.user_name,
            "tool_id": user_favorites.tool_id,
            "tool_name": home_page_tool.name,
            "description": home_page_tool.description,
            "icon_url" : home_page_tool.icon_url,
            "category_name" : home_page_tool.category_name,
            "category_id": home_page_tool.category_id,
            "url":home_page_tool.url
        }
        result_list.append(result_dict)
    # 返回JSON响应
    return jsonify(result_list)

@home_page_api_bp.route('/<string:user_name>/title', methods=['GET'])
def home_page_personal_center_title(user_name):
    # 查询出token 云集调用次数
    token_balance = TokenBalance.query.filter(TokenBalance.token_count).filter_by(domain_account=user_name).first()
    use_lobechat_count = Message.query.filter_by(domain_account=user_name).count()

    return jsonify({"token_balance":token_balance.token_count,"use_lobechat_count":use_lobechat_count})

@home_page_api_bp.route('/statistics', methods=['GET'])
@cache.cached(timeout=86400)  # 设置缓存过期时间为24小时
def home_page_statistics():
    # 查询出token 云集调用次数
    tool_num = HomePageTool.query.count()
    user_num = User_Info.query.count()
    call_time = Message.query.count()
    return jsonify({"tool_num": tool_num, "user_num": user_num, "call_time": call_time})