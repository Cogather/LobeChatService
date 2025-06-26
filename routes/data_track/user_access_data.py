from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db
from models.user_access import UserAccessInfo

user_access_api_bp = Blueprint('user_access', __name__)

@user_access_api_bp.route('',methods=['POST'])
def user_access_data_db():
    try:
        # 用户访问 首页 云集chat 打点接口
        data = request.get_json()
        access_time = datetime.now()
        access_time = access_time.strftime("%Y-%m-%d %H:%M:%S")
        user_info = UserAccessInfo(user_name=data['user_name'], access_time=access_time, access_platform=data['access_platform'])
        db.session.add(user_info)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Message added successfully',
            'data': {
                'user_access_id': user_info.id
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': 'Message added fail',
        }, 500)
    finally:
        # 手动释放资源（如果不在 Flask 请求上下文中）
        db.session.close()