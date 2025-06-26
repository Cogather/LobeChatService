import time

from models import db
from models.user_group_role_link import User_Link
from utils.model_request import generate_random_id


def common_model_user_permission(user_name):
    # 用户工号,数据库查询角色信息，进行权限校验
    user_group_role_link = User_Link.query.filter_by(user_name=user_name).first()
    if user_group_role_link:
        group = user_group_role_link.link_group_id
        role = user_group_role_link.link_role_id
        if "1" in group or int(role) >= 1:
            # 有权限
            return True
        else:
            return False
    else:
        return False
def advanced_model_user_permission(user_name):
    # 用户工号,数据库查询角色信息，进行权限校验
    user_group_role_link = User_Link.query.filter_by(user_name=user_name).first()
    if user_group_role_link:
        group = user_group_role_link.link_group_id
        role = user_group_role_link.link_role_id
        if "2" in group or int(role) >= 2:
            # 有权限
            return True
        else:
            return False
    else:
        return False

def add_notice_permission(user_name):
    # 用户工号,数据库查询角色信息，进行权限校验
    user_group_role_link = User_Link.query.filter_by(user_name=user_name).first()
    if user_group_role_link:
        role = user_group_role_link.link_role_id
        if int(role) >= 2:
            # 有权限
            return True
        else:
            return False
    else:
        return False

def no_permission_response(model):
    event_id = generate_random_id()
    created = int(time.time())
    first_data = {
        "id": event_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "service_tier": "default",
        "system_fingerprint": "fp_4691090a87",
        "choices": [{
            "index": 0,
            "delta": {"content": "您没有访问外部模型权限，如果需要，请及时申请....\n"},  # 空的delta
            "logprobs": "null",
            "finish_reason": "stop"  # 标记流结束
        }]
    }
    return first_data

def operation_page_permission(user_name):
    # 运维页面权限校验
    user_group_role_link = User_Link.query.filter_by(user_name=user_name).first()
    db.session.close()  # 确保释放连接
    if user_group_role_link is not None and int(user_group_role_link.link_role_id) >= 2:
        return True
    else:
        return False