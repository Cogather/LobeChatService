import base64
import json
import traceback

import requests
from flask import Blueprint
from config_cache import cache
from utils.constant import Constants

home_page_backend_bp = Blueprint('home_page_backend', __name__)

@home_page_backend_bp.route('/find/agent/json', methods=['POST', 'GET'])
def run_agent_model():
    print("获取agent列表")
    try:
        # 读取 JSON 文件
        with open('deploy/agent.json', 'r', encoding='utf-8') as f:
            data = json.load(f)  # data 是解析后的字典或列表
        return data
    except Exception as e:
        traceback.print_exc()  # 打印完整堆栈（包括源代码行号）
        return {"error": "agent json调用失败"}, 500

@home_page_backend_bp.route('/find/plugin/json', methods=['POST', 'GET'])
def run_plugin_model():
    print("获取plugin列表")
    # 构造请求，然后返回
    host_url = base64.b64decode(Constants.PLUGIN_URL).decode('utf-8')
    # 1. 定义缓存 key（可以更智能一点根据请求参数等生成）
    cache_key = 'run_plugin_model_cache_key'
    # 2. 查看是否已缓存
    cached_result = cache.get(cache_key)
    if cached_result:
        print("返回缓存数据")
        return cached_result
    # 3. 没命中缓存，发请求
    response = requests.get(url=host_url, verify=False)
    if response.status_code == 200:
        try:
            result = response.json()
            cache.set(cache_key, result, timeout=86400)
            return result
        except ValueError as e:
            # JSON 解析失败，不缓存
            return {"error": "无法解析 JSON 数据", "details": str(e) + response.text}, 500
    else:
        # 请求失败，不缓存
        return {"error": "plugin json请求失败", "status_code": response.status_code}, response.status_code

@home_page_backend_bp.route('/find/agent/detail/<name>/json', methods=['POST', 'GET'])
def run_agent_detail_model(name):
    print(f"获取{name}插件详情")
    cache_key = f'agent_detail_cache::{name}'
    # 尝试命中缓存
    cached_data = cache.get(cache_key)
    if cached_data:
        print("返回缓存数据")
        return cached_data
    # 发起真实请求
    url = base64.b64decode(Constants.AGENT_DEATIL_URL).decode('utf-8').format(name)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        try:
            json_data = response.json()
            cache.set(cache_key, json_data, timeout=86400)

            return json_data
        except ValueError as e:
            return {"error": "无法解析 JSON 数据", "details": str(e) + response.text}, 500
    else:
        return {"error": "agent json请求失败", "status_code": response.status_code}, response.status_code