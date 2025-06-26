import base64
import json
from collections import Counter

import requests
from flask import request, jsonify, Blueprint

from models import db
from models.user_group_role_link import User_Link
from models.user_info import User_Info
from utils.constant import Constants
from utils.response_codes import ResponseCodes

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['POST'])
def add_user_to_bd():
    success_count = 0
    insert_db_count = 0
    datas = request.get_json()
    list_user_name = []
    User_Info.query.filter_by()
    token_list = []
    for data in datas:
        # 工号带wx的，变大写
        user_name = uppercase_2nd_and_3rd(data.get("user_name"))
        list_user_name.append(user_name)
    # 执行查询,获取已经存在的人员工号
    all_usernames_tuples = db.session.query(User_Info.user_name).all()
    # 手动获取从元组中提取的第一个元素
    all_usernames = [username[0] for username in all_usernames_tuples]
    counter1 = Counter(list_user_name)
    counter2 = Counter(all_usernames)
    # 计算交集（会考虑元素的出现次数）（# 修改的人员名单）
    need_modify_user_names = list((counter1 & counter2).elements())
    # 找出 counter1 中有而 counter2 中没有的元素
    need_insert_user_names = set(counter1) - set(counter2)

    is_commit,insert_user_name_list,need_modify_user_name_list = (
        update_or_insert_data(need_modify_user_names,need_insert_user_names,datas))

    # 批量审批request_token
    for data in datas:
        if data.get("user_name") in insert_user_name_list:
            token_data = {"domain_account": data.get("user_name"), "requested_tokens": data.get("requested_tokens")}
            token_list.append(token_data)
    if is_commit:
        for token_info in token_list:
            is_success = set_default_token(token_info.get("domain_account"),token_info.get("requested_tokens"))
            if is_success:
                success_count += 1
                print("{}审批成功".format(token_info.get("domain_account")))
            else:
                print("{}审批失败".format(token_info.get("domain_account")))
    return jsonify({
        "update_count" : need_modify_user_names.__len__(),
        'insert_count':insert_user_name_list.__len__(),
        'success_count': success_count,
    }), ResponseCodes.SUCCESS_VALID

@users_bp.route('/add_or_update_user_token', methods=['POST'])
def add_or_update_user_token():
    success_count = 0
    datas = request.get_json()
    list_user_name = []
    User_Info.query.filter_by()
    token_list = []
    for data in datas:
        user_name = uppercase_2nd_and_3rd(data.get("user_name"))
        list_user_name.append(user_name)
    # 执行查询,获取已经存在的人员工号
    all_usernames_tuples = db.session.query(User_Info.user_name).all()
    # 手动获取从元组中提取的第一个元素
    all_usernames = [username[0] for username in all_usernames_tuples]
    counter1 = Counter(list_user_name)
    counter2 = Counter(all_usernames)
    # 计算交集（会考虑元素的出现次数）（# 修改的人员名单）
    need_modify_user_names = list((counter1 & counter2).elements())
    # 找出 counter1 中有而 counter2 中没有的元素
    need_insert_user_names = set(counter1) - set(counter2)

    is_commit,insert_user_name_list,need_modify_user_name_list = update_or_insert_data(need_modify_user_names,need_insert_user_names,datas)

    # 审批list
    need_approve_list = insert_user_name_list + need_modify_user_name_list
    # 批量审批request_token
    for data in datas:
        if data.get("user_name") in need_approve_list:
            token_data = {"domain_account": data.get("user_name"), "requested_tokens": data.get("requested_tokens")}
            token_list.append(token_data)
    if is_commit:
        for token_info in token_list:
            is_success = set_default_token(token_info.get("domain_account"),token_info.get("requested_tokens"))
            if is_success:
                success_count += 1
                print("{}审批成功".format(token_info.get("domain_account")))
            else:
                print("{}审批失败".format(token_info.get("domain_account")))
    return jsonify({
        "update_count" : need_modify_user_names.__len__(),
        'insert_count':insert_user_name_list.__len__(),
        'success_count': success_count,
    }), ResponseCodes.SUCCESS_VALID

@users_bp.route('/addUser', methods=['POST'])
def add_user_with_code():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({'status': 'error', 'message': 'Code is required'}), ResponseCodes.BAD_REQUEST
    # 获取 access_tokenjin
    access_token_response = get_access_token(code)
    # 检查 access_token 是否成功获取
    if isinstance(access_token_response, tuple):
        return access_token_response  # 如果是元组，说明获取 token 失败，直接返回错误响应
    access_token = access_token_response
    # # 使用access_token获取用户信息
    headers, user_info_data, user_info_url = build_args(access_token)
    try:
        user_info_response = requests.post(user_info_url, headers=headers, json=user_info_data)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
        # # 假设返回的用户信息包含这些字段：domain_account 和 chinese_name
        domain_account = user_info.get('uid')
        chinese_name = user_info.get('displayNameCn')
        # 员工人员信息获取
        dept_info = get_dept_info(domain_account)
        if dept_info is None:
            return jsonify({"error": "员工已离职"})
        # 检查用户是否已经存在
        if is_in_user_table(domain_account):
            return user_is_in_table(chinese_name, domain_account)
        else:
            user, user_link = build_user_info(dept_info, domain_account)
            is_insert = insert_to_db(user,user_link)
            is_approved = False
            if is_insert:
                # 设置默认token，并审批
                if "云核心网产品线".__eq__(user.departmentL2):
                    requested_tokens = 10000
                else:
                    requested_tokens = 0
                is_approved = set_default_token(domain_account,requested_tokens)
            else:
                return jsonify({"error": "添加用户信息失败"})
            if is_approved and is_insert:
                return success_approved(chinese_name, domain_account)
            else:
                return jsonify({"error": "审批失败"})
    except requests.exceptions.RequestException as e:
        return (jsonify({'status': 'error', 'message': 'Failed to retrieve user info'}),
                ResponseCodes.INTERNAL_SERVER_ERROR)

def uppercase_2nd_and_3rd(s):
    if len(s) >= 3:  # 确保至少有3个字符
        return s[:1] + s[1:3].upper() + s[3:]
    else:
        return s  # 如果长度 < 3，直接返回原字符串

@users_bp.route('/is_cloud_core/<user_name>', methods=['GET'])
def is_cloud_core(user_name):
    # 员工人员信息获取
    dept_info = get_dept_info(user_name)
    if dept_info is None:
        return jsonify({"error": "员工已离职"})
    else:
        if dept_info.get("departmentL2") == "云核心网产品线":
            return jsonify({"is_cloud_core": True})
        else:
            return jsonify({"is_cloud_core": False})

def build_args(access_token):
    user_info_url = base64.b64decode(Constants.USER_INFO_URL).decode('utf-8')
    headers = {
        "Content-Type": "application/json"
    }
    user_info_data = {
        "client_id": base64.b64decode(Constants.CLIENT_ID).decode('utf-8'),
        "access_token": access_token,
        "scope": "base.profile"
    }
    return headers, user_info_data, user_info_url

def user_is_in_table(chinese_name, domain_account):
    return jsonify({
        'status': 'success',
        'message': 'User is valid',
        'data': {
            'domain_account': domain_account,
            'chinese_name': chinese_name
        }
    }), ResponseCodes.SUCCESS_VALID

def success_approved(chinese_name, domain_account):
    return jsonify({
        'status': 'success',
        'message': 'User is add to table',
        'data': {
            'domain_account': domain_account,
            'chinese_name': chinese_name
        }
    }), ResponseCodes.SUCCESS_VALID

def build_user_info(dept_info, domain_account):
    # 不存在于用户表中，添加进用户表，默认普通用户,无群组
    user = User_Info(user_name=domain_account, chn_name=dept_info.get("cnName"),
                     departmentL1=dept_info.get("departmentL1"),
                     departmentL2=dept_info.get("departmentL2"),
                     departmentL3=dept_info.get("departmentL3"),
                     departmentL4=dept_info.get("departmentL4"),
                     departmentL5=dept_info.get("departmentL5"),
                     departmentL6=dept_info.get("departmentL6")
                     )
    if "云核心网产品线".__eq__(user.departmentL2):
        link_group_id = "1"
    else:
        link_group_id = "0"
    user_link = User_Link(user_name=domain_account, link_group_id=link_group_id, link_role_id='0')
    return user, user_link

def get_access_token(code):
    token_url = "https://uniportal.huawei.com/saaslogin1/oauth2/accesstoken"
    client_id = base64.b64decode(Constants.CLIENT_ID).decode('utf-8')
    client_secret = base64.b64decode(Constants.CLIENT_SECRET).decode('utf-8')
    grant_type = "authorization_code"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "https://lobechat-beta.coreai.rnd.huawei.com/chat?agent=",
        "grant_type": grant_type,
        "code": code
    }

    try:
        response = requests.post(token_url, headers=headers, json=data)
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info.get('access_token')
        if not access_token:
            return jsonify({'status': 'error', 'message': 'Failed to obtain access token'}), ResponseCodes.BAD_REQUEST
        return access_token
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), ResponseCodes.BAD_REQUEST

# 判断是否为白名单用户的函数
def is_in_user_table(domain_account):
    # 查询 User 表，检查该 domain_account 是否存在
    return User_Info.query.filter_by(user_name=domain_account).first() is not None
def insert_to_db(user,user_link):
    try:
        db.session.add(user)
        db.session.add(user_link)
        # 提交会话以保存更改到数据库
        db.session.commit()
        return True
    except Exception as e:
        # 插入异常，回滚
        db.session.rollback()
        return False
def set_default_token(domain_account,requested_tokens):
    # 设置默认token，并审批
    data = {"domain_account":domain_account,"requested_tokens":requested_tokens,"reason_for_request":"默认初始化调用"}
    request_url = "http://localhost:8000/api/token_applications"
    response = requests.post(url=request_url,json=data)
    if response.status_code == 201:
        try:
            print("提交审批")
            request_id = int(response.json().get('request_id'))
            # 审批流程
            return approve_method(request_id)
        except ValueError as e:
            return False
    else:
        return False

def approve_method(request_id):
    approve_url = "http://localhost:8000/api/token_applications/approve/{}".format(request_id)
    data = {"approved_by":"system","approval_comments":"默认初始化调用"}
    approve_response = requests.put(url=approve_url,json=data)
    if approve_response.status_code == 200:
        print("审批通过")
        return True
    else:
        return False

def get_dept_info(domain_account):
    url = base64.b64decode(Constants.FIND_USER_DEPT_URL).decode('utf-8')
    params = {
        "X-HW-ID": "com.huawei.ipd.coretool.devkit",
        "X-HW-APPKEY": base64.b64decode(Constants.X_HW_APPKEY).decode('utf-8')
    }
    data = [domain_account]
    response = requests.post(url=url, params=params, json=data)
    if response.status_code == 200:
        # 部门信息获取
        data = json.loads(response.content)[0]
        if data.get('expiredDate') is not None:
            print("人员已离职，不能进行操作")
            return None
        else:
            dept_info = {
                "cnName" : data.get('cnName'),
                "departmentL1": data.get('departname2'),
                "departmentL2": data.get('departname3'),
                "departmentL3": data.get('departname4'),
                "departmentL4": data.get('departname5'),
                "departmentL5": data.get('departname6'),
                "departmentL6": data.get('departname7'),
            }
            return dept_info
    else:
        return None

def get_dept_info_batch(user_name_list):
    user_list = []
    for user_name in user_name_list:
        user_list.append(user_name)

    url = base64.b64decode(Constants.FIND_USER_DEPT_URL).decode('utf-8')
    params = {
        "X-HW-ID": "com.huawei.ipd.coretool.devkit",
        "X-HW-APPKEY": base64.b64decode(Constants.X_HW_APPKEY).decode('utf-8')
    }
    result_info = []
    response = requests.post(url=url, params=params, json=user_list)
    if response.status_code == 200:
        # 部门信息获取
        datas = json.loads(response.content)
        for data in datas:
            if data.get('cnName') is None:
                print("{}工号有误".format(data.get("account")))
                continue
            if data.get('expiredDate') is not None:
                print("人员已离职，不能进行操作")
                continue
            else:
                dept_info = {
                    "departmentL1": data.get('departname2'),
                    "departmentL2": data.get('departname3'),
                    "departmentL3": data.get('departname4'),
                    "departmentL4": data.get('departname5'),
                    "departmentL5": data.get('departname6'),
                    "departmentL6": data.get('departname7'),
                }
                user = User_Info(user_name=data.get("account"), chn_name=data.get("cnName"),
                                 departmentL1=dept_info.get("departmentL1"),
                                 departmentL2=dept_info.get("departmentL2"),
                                 departmentL3=dept_info.get("departmentL3"),
                                 departmentL4=dept_info.get("departmentL4"),
                                 departmentL5=dept_info.get("departmentL5"),
                                 departmentL6=dept_info.get("departmentL6")
                                 )
                result_info.append(user)
    return result_info

def update_or_insert_data(need_modify_user_names,need_insert_user_names,datas):
    insert_user_group = []
    need_modify_user_groups = []
    insert_user_name_list = []
    need_modify_user_name_list = []
    # 新插入人员信息补充
    insert_user_infos = get_dept_info_batch(need_insert_user_names)
    # 过滤掉有问题人员工号的集合
    for info in insert_user_infos:
        insert_user_name_list.append(info.user_name)
    for data in datas:
        if data.get("user_name") in insert_user_name_list:
            user_link = User_Link(user_name=data.get("user_name"), link_group_id=data.get("group_id"), link_role_id='0')
            insert_user_group.append(user_link)
        if data.get("user_name") in need_modify_user_names:
            user_link = User_Link(user_name=data.get("user_name"), link_group_id=data.get("group_id"), link_role_id='0')
            need_modify_user_groups.append(user_link)
    for group in need_modify_user_groups:
        need_modify_user_name_list.append(group.user_name)
    try:
        # 表新增
        db.session.add_all(insert_user_infos)
        db.session.add_all(insert_user_group)
        for need_modify_user_group in need_modify_user_groups:
            User_Link.query.filter(
                User_Link.user_name == need_modify_user_group.user_name
            ).update({
                User_Link.link_group_id: need_modify_user_group.link_group_id
            })
        # 提交事务
        db.session.commit()
        return True,insert_user_name_list,need_modify_user_name_list
    except Exception as e:
        # 插入异常，回滚
        db.session.rollback()
        return False,insert_user_name_list,need_modify_user_groups
