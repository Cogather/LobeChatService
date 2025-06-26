
def test_anthropic_run_model(client,sample_user_link,mocker):
    data ={
          "max_tokens": 4096,
          "messages": [
            {
              "content": "你好",
              "role": "user"
            }
          ],
          "model": "claude-3-5-haiku-20241022",
          "temperature": 0.5,
          "top_p": 1,
          "stream": True
        }

    # Mock requests.post 返回成功流式响应
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [b"data: mock chunk 1\n", b"data: mock chunk 2\n"]
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('requests.post', return_value=mock_response)


    response = client.post(
        f'/api/anthropic/run/{sample_user_link.user_name}/v1/messages',
        json = data
    )
    assert response.status_code == 200


def test_deepseek_run_model(client,sample_user_link,mocker):
    data ={
            "model": "deepseek-chat",
            "stream": True,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "temperature": 0.3,
            "top_p": 1,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "1+1=？"}
            ]
        }

    # Mock requests.post 返回成功的流式响应
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [b"data: mock chunk 1\n", b"data: mock chunk 2\n"]
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('requests.post', return_value=mock_response)
    response = client.post(
        f'/api/deepseek/run/v1/{sample_user_link.user_name}/chat/completions',
        json = data
    )
    assert response.status_code == 200

def test_google_run_model(client, sample_user_link, mocker):
    # 测试数据
    data = {
        "model": "gemini-1.5-pro-002",
        "stream": True,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.3,
        "top_p": 1,
        "messages": [
            {"role": "user", "content": "1+1=？"}
        ]
    }

    # Mock requests.post 返回成功的流式响应
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [b"data: mock chunk 1\n", b"data: mock chunk 2\n"]
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('requests.post', return_value=mock_response)

    # 测试正常请求
    response = client.post(
        f'/api/google/v1/{sample_user_link.user_name}/chat/completions',
        json = data
    )
    assert response.status_code == 200

def test_kimi_run_model(client,sample_user_link,mocker):
    data ={
            "model": "moonshot-v1-128k",
            "stream": True,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 1,
            "messages": [
                {
                    "content": "你好",
                    "role": "user"
                }
            ],
            "temperature": 0.5
        }

    # Mock requests.post 返回成功的流式响应
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [b"data: mock chunk 1\n", b"data: mock chunk 2\n"]
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('requests.post', return_value=mock_response)
    response = client.post(
        f'/api/kimi/run/v1/{sample_user_link.user_name}/chat/completions',
        json = data
    )
    assert response.status_code == 200

    # 权限未通过
    sample_user_link.link_group_id = '0'
    response = client.post(
        f'/api/kimi/run/v1/{sample_user_link.user_name}/chat/completions',
        json = data
    )
    assert response.status_code == 200  # 最后检查 code

def test_open_ai_run_model(client,sample_user_link,mocker):
    data = {
            "platform_id" : "1",
            "model_scenario_name" : "advanced_could_core",
            "model": "gpt-4o",
            "stream": True,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "temperature": 0.3,
            "top_p": 1,
            "messages": [
                {"role": "user", "content": "你好？"}
            ]
        }

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [b"data: mock chunk 1\n", b"data: mock chunk 2\n"]
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('requests.post', return_value=mock_response)
    response = client.post(
        f'/api/open_ai/run/v1/{sample_user_link.user_name}/chat/completions',
        json = data
    )
    assert response.status_code == 200

    # 权限未通过
    sample_user_link.link_group_id = '0'
    response = client.post(
        f'/api/open_ai/run/v1/{sample_user_link.user_name}/chat/completions',
        json = data
    )
    assert response.status_code == 200  # 最后检查 code
