from flask import Blueprint, request, jsonify
from models.repo_permission import db, RepoPermission

repo_permissions_bp = Blueprint('repo_permissions', __name__)

# 添加仓库到白名单
@repo_permissions_bp.route('/add', methods=['POST'])
def add_permission():
    """添加仓库到白名单"""
    data = request.get_json()

    repo_name = data.get('repo_name')

    # 参数检查
    if not repo_name:
        return jsonify({
            "success": False,
            "message": "缺少必要参数"
        }), 400

    # 检查仓库是否已存在
    existing_permission = RepoPermission.query.filter_by(repo_name=repo_name).first()
    if existing_permission:
        return jsonify({
            "success": False,
            "message": "该仓库已经在白名单中"
        }), 409

    # 新增仓库到白名单
    permission = RepoPermission(repo_name=repo_name)
    db.session.add(permission)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "白名单仓库添加成功"
    }), 201

# 从白名单移除仓库
@repo_permissions_bp.route('/remove', methods=['POST'])
def remove_permission():
    """从白名单移除仓库"""
    data = request.get_json()

    repo_name = data.get('repo_name')

    # 参数检查
    if not repo_name:
        return jsonify({
            "success": False,
            "message": "缺少必要参数"
        }), 400

    # 查找并删除仓库
    permission = RepoPermission.query.filter_by(repo_name=repo_name).first()
    if permission:
        db.session.delete(permission)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "白名单仓库删除成功"
        })
    else:
        return jsonify({
            "success": False,
            "message": "未找到该仓库白名单记录"
        }), 404


# 检查仓库是否在白名单中
@repo_permissions_bp.route('/check', methods=['POST'])
def check_permission():
    """检查多个仓库是否都在白名单中"""
    data = request.get_json()

    repo_names = data.get('repo_name')

    # 参数检查
    if not repo_names or not isinstance(repo_names, list):
        return jsonify({
            "success": False,
            "message": "缺少必要参数或参数格式错误"
        }), 400

    # 检查每个仓库是否在白名单中
    missing_repos = []  # 存放不在白名单中的仓库名称
    for repo_name in repo_names:
        permission = RepoPermission.query.filter_by(repo_name=repo_name).first()
        if not permission:
            missing_repos.append(repo_name)

    # 如果有仓库不在白名单中，返回通用的失败信息
    if missing_repos:
        return jsonify({
            "has_permission": False,
            "message": "仓库白名单校验失败"
        }), 404

    # 所有仓库都在白名单中
    return jsonify({
        "has_permission": True,
        "message": "仓库白名单校验成功"
    })