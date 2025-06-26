import requests
def test_add_user_to_bd(client, mocker, sample_user_info_tool):
    def mock_requests_post_side_effect(url, *args, **kwargs):
        if url == "http://localhost:8000/api/token_applications":
            mock_response = mocker.Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {'request_id': 123}
            return mock_response
        elif url == "http://localhost:8000/api/token_applications/approve/123":
            mock_response = mocker.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'status': 'approved'}
            return mock_response
        else:
            # 对于其他 URL，使用真实的 requests.post
            # 创建一个新的 Session 来绕过 mock
            session = requests.Session()
            return session.post(url, *args, **kwargs)

    # 使用 side_effect 动态控制 mock 行为
    mock_requests_post = mocker.patch('requests.post', side_effect=mock_requests_post_side_effect)
    mock_requests_put = mocker.patch('requests.put', side_effect=mock_requests_post_side_effect)

    mock_requests_post.return_value = mock_requests_post
    mock_requests_put.return_value = mock_requests_put
    # 构造请求数据
    data = [
        {
            "user_name": "test_name",
            "requested_tokens": 100000,
            "group_id": "1,2"
        },
        {
            "user_name": "g60062050",
            "requested_tokens": 100000,
            "group_id": "1,2"
        }
    ]

    # 调用接口
    response = client.post('/api/users', json=data)

    # 验证响应
    assert response.status_code == 201

def test_add_user_with_code(client, mocker, sample_user_info_tool):
    def mock_requests_post_side_effect(url, *args, **kwargs):
        if url == "https://uniportal.huawei.com/saaslogin1/oauth2/accesstoken":
            mock_response = mocker.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'access_token': "aaa"}
            return mock_response
        elif url == "https://uniportal.huawei.com/saaslogin1/oauth2/userinfo":
            mock_response = mocker.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'uid': 'g60062050','displayNameCn':'耿贺康'}
            return mock_response
        elif url == "http://localhost:8000/api/token_applications":
            mock_response = mocker.Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {'request_id': 123}
            return mock_response
        elif url == "http://localhost:8000/api/token_applications/approve/123":
            mock_response = mocker.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'status': 'approved'}
            return mock_response
        else:
            # 对于其他 URL，使用真实的 requests.post
            # 创建一个新的 Session 来绕过 mock
            session = requests.Session()
            return session.post(url, *args, **kwargs)

    # 使用 side_effect 动态控制 mock 行为
    mock_requests_post = mocker.patch('requests.post', side_effect=mock_requests_post_side_effect)
    mock_requests_put = mocker.patch('requests.put', side_effect=mock_requests_post_side_effect)
    mock_requests_put.return_value = mock_requests_put
    mock_requests_post.return_value = mock_requests_post
    # 调用接口
    data = {"code":"111"}
    response = client.post('/api/users/addUser', json=data)
    # 验证响应
    assert response.status_code == 201