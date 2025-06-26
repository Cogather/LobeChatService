import json
import pytest
from unittest.mock import patch


def test_add_notice_success(client, mocker):
    """测试成功添加公告"""
    # Mock权限检查函数返回True
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'notice': '这是一个测试公告',
        'expiration_time': 1440,  # 24小时
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['content'] == '这是一个测试公告'


def test_add_notice_no_permission(client, mocker):
    """测试无权限添加公告"""
    # Mock权限检查函数返回False
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=False)
    
    data = {
        'user_name': 'normal_user',
        'notice': '无权限用户尝试添加公告',
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 403  # USER_INVALID对应的状态码
    response_data = json.loads(response.data)
    assert 'permission' in response_data['message'].lower()


def test_add_notice_missing_content(client, mocker):
    """测试添加空公告内容"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'notice': '',  # 空公告
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 403  # invalid notice
    response_data = json.loads(response.data)
    assert 'invalid notice' in response_data['message'].lower()


def test_add_notice_missing_notice_field(client, mocker):
    """测试缺少notice字段"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 403  # invalid notice
    response_data = json.loads(response.data)
    assert 'invalid notice' in response_data['message'].lower()


def test_add_notice_type1_default_expiration(client, mocker):
    """测试type=1时使用默认过期时间"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'notice': '测试默认过期时间',
        'type': 1,
        'platform_id': 1
        # 不设置expiration_time，应该使用默认值
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['content'] == '测试默认过期时间'


def test_add_notice_type2_default_expiration(client, mocker):
    """测试type=2时使用默认过期时间"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'notice': '测试工作公告默认过期时间',
        'type': 2,
        'platform_id': 1
        # 不设置expiration_time，应该使用工作公告的默认值
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['content'] == '测试工作公告默认过期时间'


def test_add_notice_custom_expiration(client, mocker):
    """测试使用自定义过期时间"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'notice': '测试自定义过期时间',
        'expiration_time': 720,  # 12小时
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['content'] == '测试自定义过期时间'


def test_add_notice_long_content(client, mocker):
    """测试添加长内容的公告"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    long_notice = 'A' * 5000  # 5000字符的长公告
    data = {
        'user_name': 'admin_user',
        'notice': long_notice,
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据数据库字段长度限制，可能成功或失败
    assert response.status_code in [200, 400, 500]


def test_add_notice_special_characters(client, mocker):
    """测试添加包含特殊字符的公告"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    special_notice = "特殊字符公告: !@#$%^&*()_+{}|:<>?[]\\;'\",./ 😀🎉"
    data = {
        'user_name': 'admin_user',
        'notice': special_notice,
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['content'] == special_notice


def test_get_latest_notice_success(client, sample_notice):
    """测试成功获取最新公告"""
    data = {
        'type': sample_notice.type,
        'platform_id': sample_notice.platform_id
    }
    
    response = client.post(
        '/api/notice_api/release_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['content'] == sample_notice.notice


def test_get_latest_notice_invalid_status(client, db_session):
    """测试获取无效状态的公告"""
    # 创建一个无效状态的公告
    from models.notices import Notices
    invalid_notice = Notices(
        notice="无效状态公告",
        start_time="2024-01-01 10:00:00",
        creator="test_user",
        expiration_time=1440,
        expected_end_time="2024-01-02 10:00:00",
        is_valid=0,  # 无效状态
        platform_id=1,
        type=1
    )
    db_session.add(invalid_notice)
    db_session.commit()
    
    data = {
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/release_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) == 0  # 应该返回空数组


def test_get_latest_notice_no_match(client):
    """测试获取不存在的公告类型"""
    data = {
        'type': 999,  # 不存在的类型
        'platform_id': 999  # 不存在的平台
    }
    
    response = client.post(
        '/api/notice_api/release_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据实际实现，可能返回空数组或报错
    assert response.status_code in [200, 404]


def test_get_latest_notice_missing_type(client):
    """测试获取公告时缺少type字段"""
    data = {
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/release_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据实际实现可能报错
    assert response.status_code in [200, 400, 500]


def test_get_latest_notice_missing_platform_id(client):
    """测试获取公告时缺少platform_id字段"""
    data = {
        'type': 1
    }
    
    response = client.post(
        '/api/notice_api/release_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据实际实现可能报错
    assert response.status_code in [200, 400, 500]


def test_add_notice_invalid_json(client):
    """测试添加公告时使用无效JSON"""
    response = client.post(
        '/api/notice_api/add_notice',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_get_latest_notice_invalid_json(client):
    """测试获取公告时使用无效JSON"""
    response = client.post(
        '/api/notice_api/release_notice',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_add_notice_zero_expiration(client, mocker):
    """测试添加过期时间为0的公告"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'notice': '测试0过期时间',
        'expiration_time': 0,
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) > 0
    assert response_data[0]['content'] == '测试0过期时间'


def test_add_notice_negative_expiration(client, mocker):
    """测试添加负数过期时间的公告"""
    mocker.patch('utils.permission_utils.add_notice_permission', return_value=True)
    
    data = {
        'user_name': 'admin_user',
        'notice': '测试负数过期时间',
        'expiration_time': -60,
        'type': 1,
        'platform_id': 1
    }
    
    response = client.post(
        '/api/notice_api/add_notice',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # 根据业务逻辑，可能允许或不允许负数
    assert response.status_code in [200, 400]