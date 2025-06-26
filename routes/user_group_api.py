import requests
from flask import Blueprint, request, jsonify

from models import db
from models.group_permission_records import GroupApplication
from models.user_group_role_link import User_Link

user_group_bp = Blueprint('user_group_api', __name__)

@user_group_bp.route("/update_group",methods=['POST'])
def update_user_group():
    data = request.get_json()
    user_link_info = User_Link.query.filter_by(user_name=data.get("applicant")).first()
    group_id = user_link_info.link_group_id
    if data.get('modify_group') in group_id:
        return {"message":"用户已有当前权限"}
    try:
        # 构建请求记录
        group_application = GroupApplication(user_name=data.get('applicant'),requested_status="pending",
                                             modify_group=data.get('modify_group'),
                                             reason_for_request=data.get('approval_comments'),operate_type="add")
        db.session.add(group_application)
        db.session.commit()
        new_request_id = group_application.id
        return {"message":"successful add records",'request_id': new_request_id}  # 返回新插入记录的主键}
    except Exception as e:
        return {"message": str(e)}

@user_group_bp.route("/remove_group",methods=['POST'])
def remove_user_group():
    data = request.get_json()
    user_link_info = User_Link.query.filter_by(user_name=data['applicant']).first()
    group_id = user_link_info.link_group_id
    if data.get('modify_group') not in group_id:
        return {"message":"用户已无当前权限"}
    # 查找用户，看看有权限没，有的话就不处理，没有的话加权限
    try:
        # 构建请求记录
        group_application = GroupApplication(user_name=data.get('applicant'),requested_status="pending",
                                             modify_group=data.get('modify_group'),
                                             reason_for_request=data.get('approval_comments'),operate_type="delete")
        db.session.add(group_application)
        db.session.commit()
        new_request_id = group_application.id
        return {"message":"successful add records",'request_id': new_request_id}  # 返回新插入记录的主键}
    except Exception as e:
        return {"message": str(e)}

@user_group_bp.route("/approval_permission/<int:request_id>",methods=['POST'])
def approval_permission_change(request_id):
    data = request.get_json()
    try:
        group_application = GroupApplication.query.filter_by(id=request_id).first()
        if group_application:
            # 如果申请已经审批通过，则直接返回
            if group_application.requested_status == 'approved':
                return jsonify({'message': 'This application has already been approved'}), 400

            # 审批通过
            group_application.requested_status = 'approved'
            group_application.approved_by = data.get('approved_by')
            group_application.approved_at = db.func.now()
            group_application.approval_comments = data.get('approval_comments', '')

            # 获取对应用户的 TokenBalance 记录
            # 审批通过，更改权限
            user_link_info = User_Link.query.filter_by(user_name=group_application.user_name).first()
            group_id = user_link_info.link_group_id
            if group_application.operate_type == 'add':
                group_id = group_id + "," + str(group_application.modify_group)
                user_link_info.link_group_id = group_id
            else:
                group_list = group_id.split(',')
                # 2. 删除元素 '3'，如果存在的话
                group_list.remove(str(group_application.modify_group))
                # 3. 用逗号拼接回字符串
                group_id_str = ','.join(group_list)
                user_link_info.link_group_id = group_id_str
            db.session.commit()
            return {"message": "权限修改成功"}
        else:
            return jsonify({'message': 'Token application not found'}), 404
    except Exception as e:
        db.session.rollback()
        print(f"error:{e}")
        return {"message":"审批失败"}


@user_group_bp.route("/add_or_remove_group", methods=['POST'])
def auto_add_approval_permission_change():
    data = request.get_json()
    records_data = {
        "applicant":data.get('applicant'),
        "approval_comments": data.get('approval_comments'),
        "modify_group":data.get('modify_group')
    }
    if data.get('type') == 'add' :
        response = requests.post("http://localhost:8000/api/user_group_api/update_group",json=records_data)
    else:
        response = requests.post("http://localhost:8000/api/user_group_api/remove_group", json=records_data)
    if response.status_code == 200:
        new_data = {"approved_by":"system","approval_comments":"系统默认审批"}
        # 自动审批
        request_id = response.json().get("request_id")
        approve_response = requests.post(f"http://localhost:8000/api/user_group_api/approval_permission/{request_id}", json=new_data)
        if approve_response.status_code == 200:
            print("审批通过")
            return {"message":"success"}
        else:
            return {"message": "审批失败"}
    else:
        return {"message": "申请失败"}


