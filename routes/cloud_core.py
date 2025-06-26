from flask import Blueprint, request, jsonify
import openai

cloud_core_bp = Blueprint('cloud_core', __name__)

@cloud_core_bp.route('/run/<string:domain_account>/chat/completions', methods=['POST'])
def run_model_with_account(domain_account):
    """运行模型的API端点（用户账号版本）"""
    try:
        data = request.get_json()
        model = data.get('model', 'DeepSeek-V3')
        
        # 这里应该有权限验证逻辑
        # 暂时使用简单的实现
        
        response = openai.ChatCompletion.create(**data)
        
        return jsonify({
            'status': 'success',
            'data': response
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@cloud_core_bp.route('/run/api_packaging/v1/chat/completions', methods=['POST'])
def run_model_with_packaging():
    """运行模型的API端点（封装版本）"""
    try:
        # 检查Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'status': 'error',
                'message': 'Invalid authorization header'
            }), 401
            
        data = request.get_json()
        model = data.get('model', 'DeepSeek-V3')
        
        response = openai.ChatCompletion.create(**data)
        
        return jsonify({
            'status': 'success',
            'data': response
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500