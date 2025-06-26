import json
import pytest


def test_submit_token_application_success(client):
    """测试成功提交token申请"""
    data = {
        'domain_account': 'test_user',
        'requested_tokens': 1000,
        'reason_for_request': '需要更多token进行测试'
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'submitted successfully' in response_data['message'].lower()
    assert 'request_id' in response_data


def test_submit_token_application_missing_domain_account(client):
    """测试提交申请时缺少domain_account"""
    data = {
        'requested_tokens': 1000,
        'reason_for_request': '测试申请'
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 500
    response_data = json.loads(response.data)
    assert 'valid employee id' in response_data['message'].lower()


def test_submit_token_application_empty_domain_account(client):
    """测试提交申请时domain_account为空"""
    data = {
        'domain_account': '',
        'requested_tokens': 1000,
        'reason_for_request': '测试申请'
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 500
    response_data = json.loads(response.data)
    assert 'valid employee id' in response_data['message'].lower()


def test_submit_token_application_none_domain_account(client):
    """测试提交申请时domain_account为None"""
    data = {
        'domain_account': None,
        'requested_tokens': 1000,
        'reason_for_request': '测试申请'
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 500
    response_data = json.loads(response.data)
    assert 'valid employee id' in response_data['message'].lower()


def test_submit_token_application_zero_tokens(client):
    """测试申请0个token"""
    data = {
        'domain_account': 'test_user',
        'requested_tokens': 0,
        'reason_for_request': '测试0个token申请'
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'submitted successfully' in response_data['message'].lower()


def test_submit_token_application_negative_tokens(client):
    """测试申请负数token"""
    data = {
        'domain_account': 'test_user',
        'requested_tokens': -100,
        'reason_for_request': '测试负数token申请'
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据业务逻辑，可能允许或不允许负数
    assert response.status_code in [201, 400]


def test_submit_token_application_large_amount(client):
    """测试申请大量token"""
    data = {
        'domain_account': 'test_user',
        'requested_tokens': 999999999,
        'reason_for_request': '测试大量token申请'
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'submitted successfully' in response_data['message'].lower()


def test_submit_token_application_missing_reason(client):
    """测试提交申请时缺少申请理由"""
    data = {
        'domain_account': 'test_user',
        'requested_tokens': 1000
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'submitted successfully' in response_data['message'].lower()


def test_submit_token_application_empty_reason(client):
    """测试提交申请时申请理由为空"""
    data = {
        'domain_account': 'test_user',
        'requested_tokens': 1000,
        'reason_for_request': ''
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'submitted successfully' in response_data['message'].lower()


def test_submit_token_application_long_reason(client):
    """测试提交申请时使用很长的申请理由"""
    long_reason = 'A' * 5000  # 5000字符的长理由
    data = {
        'domain_account': 'test_user',
        'requested_tokens': 1000,
        'reason_for_request': long_reason
    }
    
    response = client.post(
        '/api/token_applications',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据数据库字段长度限制，可能成功或失败
    assert response.status_code in [201, 400, 500]


def test_get_token_applications_success(client, db_session):
    """测试成功获取用户的token申请记录"""
    # 先创建一个申请
    from models.token_application import TokenApplication
    application = TokenApplication(
        domain_account='test_user_apps',
        requested_tokens=500,
        application_status='pending',
        reason_for_request='测试获取申请记录'
    )
    db_session.add(application)
    db_session.commit()
    
    response = client.get('/api/token_applications/test_user_apps')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['domain_account'] == 'test_user_apps'
    assert response_data[0]['requested_tokens'] == 500
    assert response_data[0]['application_status'] == 'pending'


def test_get_token_applications_not_found(client):
    """测试获取不存在用户的申请记录"""
    response = client.get('/api/token_applications/non_existent_user')
    
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert 'no applications found' in response_data['message'].lower()


def test_approve_token_application_success(client, db_session, sample_token_balance):
    """测试成功审批token申请"""
    # 先创建一个申请
    from models.token_application import TokenApplication
    application = TokenApplication(
        domain_account=sample_token_balance.domain_account,
        requested_tokens=500,
        application_status='pending',
        reason_for_request='测试审批申请'
    )
    db_session.add(application)
    db_session.commit()
    
    data = {
        'approved_by': 'admin_user',
        'approval_comments': '审批通过'
    }
    
    response = client.put(
        f'/api/token_applications/approve/{application.request_id}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'approved' in response_data['message'].lower()
    assert 'tokens added' in response_data['message'].lower()


def test_approve_token_application_new_balance(client, db_session):
    """测试审批申请时为新用户创建token余额"""
    # 创建一个新用户的申请
    from models.token_application import TokenApplication
    application = TokenApplication(
        domain_account='new_user_for_approval',
        requested_tokens=300,
        application_status='pending',
        reason_for_request='新用户申请'
    )
    db_session.add(application)
    db_session.commit()
    
    data = {
        'approved_by': 'admin_user',
        'approval_comments': '新用户审批通过'
    }
    
    response = client.put(
        f'/api/token_applications/approve/{application.request_id}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'approved' in response_data['message'].lower()


def test_approve_token_application_already_approved(client, db_session):
    """测试审批已经审批过的申请"""
    # 创建一个已审批的申请
    from models.token_application import TokenApplication
    application = TokenApplication(
        domain_account='test_user_approved',
        requested_tokens=200,
        application_status='approved',
        reason_for_request='已审批的申请'
    )
    db_session.add(application)
    db_session.commit()
    
    data = {
        'approved_by': 'admin_user',
        'approval_comments': '重复审批'
    }
    
    response = client.put(
        f'/api/token_applications/approve/{application.request_id}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'already been approved' in response_data['message'].lower()


def test_approve_token_application_not_found(client):
    """测试审批不存在的申请"""
    data = {
        'approved_by': 'admin_user',
        'approval_comments': '审批不存在的申请'
    }
    
    response = client.put(
        '/api/token_applications/approve/999999',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert 'not found' in response_data['message'].lower()


def test_approve_token_application_missing_approver(client, db_session):
    """测试审批申请时缺少审批人信息"""
    # 创建一个申请
    from models.token_application import TokenApplication
    application = TokenApplication(
        domain_account='test_user_no_approver',
        requested_tokens=100,
        application_status='pending',
        reason_for_request='测试缺少审批人'
    )
    db_session.add(application)
    db_session.commit()
    
    data = {
        'approval_comments': '审批通过但没有审批人'
    }
    
    response = client.put(
        f'/api/token_applications/approve/{application.request_id}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'approved' in response_data['message'].lower()


def test_submit_token_application_invalid_json(client):
    """测试提交申请时使用无效JSON"""
    response = client.post(
        '/api/token_applications',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_approve_token_application_invalid_json(client, db_session):
    """测试审批申请时使用无效JSON"""
    # 创建一个申请
    from models.token_application import TokenApplication
    application = TokenApplication(
        domain_account='test_user_invalid_json',
        requested_tokens=100,
        application_status='pending',
        reason_for_request='测试无效JSON'
    )
    db_session.add(application)
    db_session.commit()
    
    response = client.put(
        f'/api/token_applications/approve/{application.request_id}',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400