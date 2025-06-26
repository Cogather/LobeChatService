import json

def test_create_session_success(client, sample_user_info_tool):
    """测试成功创建会话"""
    data = {
        'session_id': 'test_session',
        'session_name': '测试会话',
        'initial_persona': '技术专家',
        'topics': '',
        'domain_account': sample_user_info_tool.user_name
    }

    response = client.post(
        '/api/sessions',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['session_id'] == 'test_session'


def test_update_session_success(client, sample_session):
    """测试成功更新会话"""
    data = {
        'session_name': '更新后的会话名称',
        'initial_persona': '产品经理'
    }

    response = client.put(
        f'/api/sessions/{sample_session.session_id}',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['session_name'] == '更新后的会话名称'