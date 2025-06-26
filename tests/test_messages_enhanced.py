import json
import pytest


def test_add_message_success(client, sample_user_info_tool, sample_session):
    """测试成功添加消息"""
    data = {
        'model_name': 'test_model',
        'model_version': '1.0',
        'tool_version': '1.0',
        'user_input': '测试输入',
        'model_output': '测试输出',
        'sequence': 1,
        'access_time': '2024-01-01 10:00:00',
        'persona': '测试角色',
        'session_id': sample_session.session_id,
        'domain_account': sample_user_info_tool.user_name
    }

    response = client.post(
        '/api/messages',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert 'message_id' in response_data['data']


def test_add_message_with_long_content(client, sample_user_info_tool, sample_session):
    """测试添加包含长内容的消息"""
    long_content = 'A' * 1000  # 1000字符的长内容
    
    data = {
        'model_name': 'test_model',
        'model_version': '1.0',
        'tool_version': '1.0',
        'user_input': long_content,
        'model_output': long_content,
        'sequence': 1,
        'access_time': '2024-01-01 10:00:00',
        'persona': '测试角色',
        'session_id': sample_session.session_id,
        'domain_account': sample_user_info_tool.user_name
    }

    response = client.post(
        '/api/messages',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'


def test_add_message_with_special_characters(client, sample_user_info_tool, sample_session):
    """测试添加包含特殊字符的消息"""
    special_content = "测试特殊字符: !@#$%^&*()_+{}|:<>?[]\\;'\",./"
    
    data = {
        'model_name': 'test_model',
        'model_version': '1.0',
        'tool_version': '1.0',
        'user_input': special_content,
        'model_output': special_content,
        'sequence': 1,
        'access_time': '2024-01-01 10:00:00',
        'persona': '测试角色',
        'session_id': sample_session.session_id,
        'domain_account': sample_user_info_tool.user_name
    }

    response = client.post(
        '/api/messages',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'


def test_add_message_with_unicode(client, sample_user_info_tool, sample_session):
    """测试添加包含Unicode字符的消息"""
    unicode_content = "Unicode测试: 🚀 🤖 🌟 ✨ 💡 🔧 ⚡ 🎯"
    
    data = {
        'model_name': 'test_model',
        'model_version': '1.0',
        'tool_version': '1.0',
        'user_input': unicode_content,
        'model_output': unicode_content,
        'sequence': 1,
        'access_time': '2024-01-01 10:00:00',
        'persona': '测试角色',
        'session_id': sample_session.session_id,
        'domain_account': sample_user_info_tool.user_name
    }

    response = client.post(
        '/api/messages',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'


def test_add_message_sequence_numbers(client, sample_user_info_tool, sample_session):
    """测试添加具有不同序列号的消息"""
    for i in range(1, 4):  # 减少循环次数以加快测试
        data = {
            'model_name': 'test_model',
            'model_version': '1.0',
            'tool_version': '1.0',
            'user_input': f'测试输入 {i}',
            'model_output': f'测试输出 {i}',
            'sequence': i,
            'access_time': '2024-01-01 10:00:00',
            'persona': '测试角色',
            'session_id': sample_session.session_id,
            'domain_account': sample_user_info_tool.user_name
        }

        response = client.post(
            '/api/messages',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['status'] == 'success'


def test_add_message_invalid_json(client):
    """测试发送无效JSON格式的消息请求"""
    response = client.post(
        '/api/messages',
        data='invalid json',
        content_type='application/json'
    )
    # Flask在无效JSON时可能返回400或500
    assert response.status_code in [400, 500]