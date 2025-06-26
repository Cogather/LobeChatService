import json
import pytest
from datetime import datetime


def test_create_session_missing_required_fields(client):
    """测试创建会话时缺少必需字段"""
    # 缺少session_id
    data = {
        'session_name': '测试会话',
        'topics': '',
        'domain_account': 'test_user'
    }
    response = client.post(
        '/api/sessions',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400

    # 缺少session_name
    data = {
        'session_id': 'test_session',
        'topics': '',
        'domain_account': 'test_user'
    }
    response = client.post(
        '/api/sessions',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_create_session_with_custom_creation_time(client, sample_user_info_tool):
    """测试使用自定义创建时间创建会话"""
    custom_time = '2024-01-01T10:00:00'
    data = {
        'session_id': 'test_session_custom_time',
        'session_name': '自定义时间会话',
        'initial_persona': '技术专家',
        'topics': 'AI,测试',
        'domain_account': sample_user_info_tool.user_name,
        'creation_time': custom_time
    }

    response = client.post(
        '/api/sessions',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['session_id'] == 'test_session_custom_time'


def test_create_session_duplicate_id(client, sample_user_info_tool, sample_session):
    """测试创建重复session_id的会话"""
    data = {
        'session_id': sample_session.session_id,  # 使用已存在的session_id
        'session_name': '重复会话',
        'topics': '',
        'domain_account': sample_user_info_tool.user_name
    }

    response = client.post(
        '/api/sessions',
        data=json.dumps(data),
        content_type='application/json'
    )
    # 应该返回错误，因为session_id已存在
    assert response.status_code == 400 or response.status_code == 500


def test_update_session_not_found(client):
    """测试更新不存在的会话"""
    data = {
        'session_name': '更新不存在的会话',
        'initial_persona': '测试角色'
    }

    response = client.put(
        '/api/sessions/non_existent_session',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 404


def test_update_session_partial_update(client, sample_session):
    """测试部分更新会话（只更新部分字段）"""
    data = {
        'session_name': '仅更新名称'
    }

    response = client.put(
        f'/api/sessions/{sample_session.session_id}',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['session_name'] == '仅更新名称'


def test_update_session_empty_data(client, sample_session):
    """测试使用空数据更新会话"""
    data = {}

    response = client.put(
        f'/api/sessions/{sample_session.session_id}',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    # 原始数据应保持不变
    assert response_data['data']['session_name'] == sample_session.session_name


def test_create_session_invalid_json(client):
    """测试发送无效JSON格式的请求"""
    response = client.post(
        '/api/sessions',
        data='invalid json',
        content_type='application/json'
    )
    assert response.status_code == 400


def test_update_session_invalid_json(client, sample_session):
    """测试发送无效JSON格式的更新请求"""
    response = client.put(
        f'/api/sessions/{sample_session.session_id}',
        data='invalid json',
        content_type='application/json'
    )
    assert response.status_code == 400


def test_create_session_with_all_fields(client, sample_user_info_tool):
    """测试创建包含所有字段的会话"""
    data = {
        'session_id': 'test_session_all_fields',
        'session_name': '完整字段会话',
        'initial_persona': '资深专家',
        'topics': 'AI,机器学习,深度学习',
        'domain_account': sample_user_info_tool.user_name,
        'creation_time': '2024-02-01T15:30:00'
    }

    response = client.post(
        '/api/sessions',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['session_id'] == 'test_session_all_fields'
    assert response_data['data']['session_name'] == '完整字段会话'


def test_update_session_all_fields(client, sample_session):
    """测试更新会话的所有可更新字段"""
    data = {
        'session_name': '全面更新的会话',
        'initial_persona': '全栈工程师',
        'topics': '前端,后端,数据库,DevOps'
    }

    response = client.put(
        f'/api/sessions/{sample_session.session_id}',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['session_name'] == '全面更新的会话'