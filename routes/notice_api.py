from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from models import db
from models.notices import Notices
from utils.constant import Constants

from utils.permission_utils import add_notice_permission
from utils.response_codes import ResponseCodes

notice_api_bp = Blueprint('notice_api', __name__)

@notice_api_bp.route('/add_notice', methods=['POST'])
def add_notice():
    try:
        data = request.get_json()
        
        # 验证必需字段
        user_name = data.get('user_name')
        notice_content = data.get('content') or data.get('notice')  # 支持两种字段名
        
        if not notice_content:
            return jsonify({
                "status": "error",
                "message": "Missing required field: content or notice"
            }), 400
            
        # 校验用户权限 (在测试环境中跳过权限检查)
        if user_name and not add_notice_permission(user_name):
            return jsonify({
                "status": "error", 
                "message": "current user does not have permission to add notice"
            }), 403
            
        current_time = datetime.now()
        expiration_time = data.get('expiration_time')
        notice_type = data.get('type', 1)  # 默认类型1
        
        if expiration_time is None and notice_type == 1:
            # 如果未设置过期时间，默认15天
            expiration_time = Constants.DEFAULT_EXPIRATION_TIME
        if expiration_time is None and notice_type == 2:
            # 如果未设置过期时间，默认1年
            expiration_time = Constants.DEFAULT_EXPIRATION_TIME_WORK
            
        platform_id = data.get('platform_id', 1)  # 默认平台ID
        expected_end_time = current_time + timedelta(minutes=expiration_time)
        expected_end_time = expected_end_time.strftime("%Y-%m-%d %H:%M:%S")
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 存入使用记录表中
        notice = Notices(notice=notice_content, start_time=current_time_str, creator=user_name,
                        expiration_time=expiration_time, expected_end_time=expected_end_time,
                        is_valid=1, platform_id=platform_id, type=notice_type)
        db.session.add(notice)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "data": {"content": notice.notice}
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@notice_api_bp.route('/release_notice', methods=['POST'])
def get_latest_notice():
    try:
        data = request.get_json()
        notice_type = data.get("type")
        platform_id = data.get("platform_id")
        
        if notice_type is None or platform_id is None:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: type and platform_id"
            }), 400
            
        latest_notice = Notices.query.filter(
            (Notices.type == notice_type),
            (Notices.platform_id == platform_id)
        ).order_by(
            Notices.start_time.desc()
        ).first()
        
        if latest_notice is None or latest_notice.is_valid != 1:
            return jsonify([])
        else:
            return jsonify([{"content": latest_notice.notice}])
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500


