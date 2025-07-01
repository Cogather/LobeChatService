from flask import Blueprint, request, jsonify, stream_template, Response
import json

cloud_core_bp = Blueprint('cloud_core', __name__)

@cloud_core_bp.route('/run/<user_name>/chat/completions', methods=['POST'])
def run_chat_completions_with_user(user_name):
    """用户聊天完成API"""
    try:
        data = request.get_json()
        # 基本响应格式
        response_data = {
            "id": "chatcmpl-xxxx",
            "object": "chat.completion.chunk",
            "created": 1711111111,
            "model": data.get("model", "default"),
            "choices": [
                {
                    "delta": {"role": "assistant", "content": "测试响应"},
                    "index": 0,
                    "finish_reason": None
                }
            ]
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cloud_core_bp.route('/run/api_packaging/v1/chat/completions', methods=['POST'])
def run_api_packaging_chat_completions():
    """API封装聊天完成"""
    try:
        data = request.get_json()
        auth_header = request.headers.get('Authorization', '')
        
        # 基本响应格式
        response_data = {
            "id": "chatcmpl-xxxx",
            "object": "chat.completion.chunk", 
            "created": 1711111111,
            "model": data.get("model", "default"),
            "choices": [
                {
                    "delta": {"role": "assistant", "content": "API封装测试响应"},
                    "index": 0,
                    "finish_reason": None
                }
            ]
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500