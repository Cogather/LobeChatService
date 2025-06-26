import base64

import requests
from flask import Blueprint, request, Response, jsonify

from utils.constant import Constants
from utils.permission_utils import common_model_user_permission, no_permission_response

# 创建蓝图
deepseek_bp = Blueprint('deepseek', __name__)

@deepseek_bp.route('/run/v1/<user_name>/chat/completions', methods=['POST'])
def run_model(user_name):
    data = request.get_json()
    # 转发请求到服务B
    if common_model_user_permission(user_name) is False:
        return jsonify(no_permission_response(data.get("model")))
    b_service_url = base64.b64decode(Constants.DEEPSEEK_HOST_URL).decode('utf-8').format(user_name)
    headers = {
        "Content-Type": "application/json",
    }

    # 单次请求（流式+实时状态码检测）
    response = requests.post(
        b_service_url,
        json=data,
        headers=headers,
        stream=True
    )
    # 实时检查首帧状态码
    if response.status_code != 200:
        # 非200时立即返回错误（不等待流结束）
        return jsonify(response.json()), response.status_code

    # 流式传输生成器
    def generate():
        try:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
        finally:
            response.close()  # 确保连接关闭
    return Response(generate(), content_type='text/event-stream')
