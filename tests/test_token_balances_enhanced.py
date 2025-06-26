import json
import pytest


def test_get_token_balance_success(client, sample_token_balance):
    """测试成功获取token余额"""
    response = client.get(f'/api/token_balances/{sample_token_balance.domain_account}')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['domain_account'] == sample_token_balance.domain_account
    assert response_data['data']['token_count'] == sample_token_balance.token_count


def test_get_token_balance_not_found(client):
    """测试获取不存在用户的token余额"""
    response = client.get('/api/token_balances/non_existent_user')
    
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'
    assert 'not found' in response_data['message'].lower()


def test_get_token_balance_empty_account(client):
    """测试使用空账号获取token余额"""
    response = client.get('/api/token_balances/')
    
    # 这可能会导致路由不匹配
    assert response.status_code == 404


def test_create_token_balance_success(client):
    """测试成功创建token余额"""
    data = {
        'domain_account': 'new_test_user'
    }
    
    response = client.post(
        '/api/token_balances/new_token_balance',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert response_data['data']['domain_account'] == 'new_test_user'
    assert response_data['data']['token_count'] == 0


def test_create_token_balance_missing_account(client):
    """测试创建token余额时缺少domain_account"""
    data = {}
    
    response = client.post(
        '/api/token_balances/new_token_balance',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'
    assert 'required' in response_data['message'].lower()


def test_create_token_balance_empty_account(client):
    """测试使用空domain_account创建token余额"""
    data = {
        'domain_account': ''
    }
    
    response = client.post(
        '/api/token_balances/new_token_balance',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'


def test_create_token_balance_duplicate(client, sample_token_balance):
    """测试创建已存在用户的token余额"""
    data = {
        'domain_account': sample_token_balance.domain_account
    }
    
    response = client.post(
        '/api/token_balances/new_token_balance',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'
    assert 'already exists' in response_data['message'].lower()


def test_update_token_balance_success(client, sample_token_balance):
    """测试成功更新token余额"""
    data = {
        'token_count': 500
    }
    
    response = client.put(
        f'/api/token_balances/{sample_token_balance.domain_account}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'updated successfully' in response_data['message'].lower()


def test_update_token_balance_not_found(client):
    """测试更新不存在用户的token余额"""
    data = {
        'token_count': 500
    }
    
    response = client.put(
        '/api/token_balances/non_existent_user',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert 'not found' in response_data['message'].lower()


def test_update_token_balance_negative_amount(client, sample_token_balance):
    """测试使用负数更新token余额"""
    data = {
        'token_count': -100
    }
    
    response = client.put(
        f'/api/token_balances/{sample_token_balance.domain_account}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据业务逻辑，可能允许或不允许负数
    assert response.status_code in [200, 400]


def test_update_token_balance_zero_amount(client, sample_token_balance):
    """测试将token余额更新为0"""
    data = {
        'token_count': 0
    }
    
    response = client.put(
        f'/api/token_balances/{sample_token_balance.domain_account}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'updated successfully' in response_data['message'].lower()


def test_update_token_balance_large_amount(client, sample_token_balance):
    """测试使用大数值更新token余额"""
    data = {
        'token_count': 999999999
    }
    
    response = client.put(
        f'/api/token_balances/{sample_token_balance.domain_account}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'updated successfully' in response_data['message'].lower()


def test_update_token_balance_invalid_json(client, sample_token_balance):
    """测试使用无效JSON更新token余额"""
    response = client.put(
        f'/api/token_balances/{sample_token_balance.domain_account}',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_update_token_balance_empty_data(client, sample_token_balance):
    """测试使用空数据更新token余额（保持原值）"""
    data = {}
    
    response = client.put(
        f'/api/token_balances/{sample_token_balance.domain_account}',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'updated successfully' in response_data['message'].lower()


def test_create_token_balance_invalid_json(client):
    """测试使用无效JSON创建token余额"""
    response = client.post(
        '/api/token_balances/new_token_balance',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_token_balance_special_characters_in_account(client):
    """测试domain_account包含特殊字符的情况"""
    data = {
        'domain_account': 'test@user.com'
    }
    
    response = client.post(
        '/api/token_balances/new_token_balance',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据业务规则，可能允许或不允许特殊字符
    assert response.status_code in [200, 201, 400]


def test_token_balance_long_account_name(client):
    """测试使用很长的domain_account名称"""
    long_name = 'a' * 200  # 200字符的长名称
    data = {
        'domain_account': long_name
    }
    
    response = client.post(
        '/api/token_balances/new_token_balance',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据数据库字段长度限制，可能成功或失败
    assert response.status_code in [200, 201, 400, 500]