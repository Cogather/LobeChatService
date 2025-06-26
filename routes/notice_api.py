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
    data = request.get_json()
    # 校验用户权限
    user_name = data.get('user_name')
    if not add_notice_permission(user_name):
        return jsonify({"message": "current user does not have permission to add notice"},ResponseCodes.USER_INVALID)
    current_time = datetime.now()
    notice = data.get('notice')
    expiration_time = data.get('expiration_time')
    type = data.get('type')
    if expiration_time is None and type == 1:
        # 如果未设置过期时间，默认15天
        expiration_time = Constants.DEFAULT_EXPIRATION_TIME
    if expiration_time is None and type == 2:
        # 如果未设置过期时间，默认1年
        expiration_time = Constants.DEFAULT_EXPIRATION_TIME_WORK
    platform_id = data.get('platform_id')
    expected_end_time = current_time + timedelta(minutes=expiration_time)
    expected_end_time = expected_end_time.strftime("%Y-%m-%d %H:%M:%S")
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    if not notice:
        return jsonify({ "message": "invalid notice"},ResponseCodes.USER_INVALID)
    # 存入使用记录表中
    notice = Notices(notice=notice,start_time=current_time,creator=user_name,expiration_time=expiration_time,
                     expected_end_time=expected_end_time,is_valid=1,platform_id = platform_id,type=type)
    db.session.add(notice)
    db.session.commit()
    return jsonify([{"content": notice.notice}])

@notice_api_bp.route('/release_notice', methods=['POST'])
def get_latest_notice():
    data = request.get_json()
    latest_notice = Notices.query.filter(
        (Notices.type == data.get("type")),
        (Notices.platform_id == data.get("platform_id"))
    ).order_by(
        Notices.start_time.desc()
    ).first()
    if latest_notice.is_valid != 1:
        return jsonify([])
    else:
        return jsonify([{"content": latest_notice.notice}])


