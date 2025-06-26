import json


def test_cloud_core_run_model(client,sample_user_info_tool,sample_user_link,mocker):
    data = {
        "model": "DeepSeek-V3",
        "stream": True,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.3,
        "top_p": 1,
        "messages": [
            {"role": "user", "content": "你好"}
        ]
    }

    chunk = {
        "id": "chatcmpl-xxxx",
        "object": "chat.completion.chunk",
        "created": 1711111111,
        "model": "gpt-4-turbo",
        "choices": [
            {
                "delta": {"role": "assistant", "content": "你好"},
                "index": 0,
                "finish_reason": None
            }
        ]
    }

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = json.dumps(chunk).encode('utf-8')
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('openai.resources.chat.completions.Completions.create', return_value=mock_response)
    sample_user_link.link_group_id = "1,2"
    response = client.post(
        f'/api/cloud_core/run/{sample_user_info_tool.user_name}/chat/completions',
        json = data
    )
    assert response.status_code == 200

def test_openai_ecosystem_encapsulation(client,sample_user_info_tool,sample_user_link,mocker):
    data = {
        "model": "DeepSeek-V3",
        "stream": True,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.3,
        "top_p": 1,
        "messages": [
            {"role": "user", "content": "你好"}
        ]
    }
    chunk = {
        "id": "chatcmpl-xxxx",
        "object": "chat.completion.chunk",
        "created": 1711111111,
        "model": "gpt-4-turbo",
        "choices": [
            {
                "delta": {"role": "assistant", "content": "你好"},
                "index": 0,
                "finish_reason": None
            }
        ]
    }

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = json.dumps(chunk).encode('utf-8')
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('openai.resources.chat.completions.Completions.create', return_value=mock_response)
    response = client.post(
        f'/api/cloud_core/run/api_packaging/v1/chat/completions',
        json = data,
        headers = {
                    "Authorization": "Bearer test_name"
                  }
        )
    assert response.status_code == 200