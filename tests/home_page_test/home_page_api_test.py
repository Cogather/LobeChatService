import json
from routes.home_page_api.home_page_api import get_tool_list, home_page_statistics

def test_get_tool_list(db_session,sample_home_page_tool):
    # 模拟数据库查询的返回值
    result = get_tool_list()
    # 验证结果是否符合预期
    assert result is not None

def test_home_page_statistics(db_session,sample_home_page_tool,sample_user_info_tool,sample_message):
    # 调用被测试的函数
    response = home_page_statistics()
    data = json.loads(response.get_data(as_text=True))
    assert data == {"tool_num": 1, "user_num": 1, "call_time": 2}

def test_home_page_favorites(db_session,client):
    data = {
        "is_favorites": True,
        "tool_id":1,
        "user_name":"aaa"
    }
    # 调用被测试的函数
    response = client.post(
        '/api/home_page_api/favorites',
        data = json.dumps(data),
        content_type ='application/json'
    )
    assert response.status_code == 200

    data1 = {
        "is_favorites": False,
        "tool_id": 1,
        "user_name": "aaa"
    }
    # 调用被测试的函数
    response = client.post(
        '/api/home_page_api/favorites',
        data = json.dumps(data1),
        content_type = 'application/json'
    )
    assert response.status_code == 200

def test_home_page_personal_center(db_session,client,sample_user_favorites_data):
    """测试个人中心查询数据"""
    # 调用被测试的函数
    response = client.get(
        f'/api/home_page_api/{sample_user_favorites_data.user_name}',
    )
    assert response.status_code == 200

def test_home_page_personal_center_title(db_session,client,sample_token_balance,sample_message,
                                         sample_user_favorites_data):
    response = client.get(
        f'/api/home_page_api/{sample_user_favorites_data.user_name}/title',
    )
    assert response.status_code == 200

def test_add_tool(db_session,client):
    data = {
        "name":"ghk-test",
        "category_id":"1",
        "category_name":"test",
        "description":"测试调用",
        "url":"aaa",
        "favorites":3,
        "image_url":"bbb",
        "icon_url":"ccc",
        "tags":"fff"
        }
    response = client.post(
        f'/api/home_page_api/add_tool',
        json=data
    )
    assert response.status_code == 200

def test_remove_tool(db_session,client,sample_home_page_tool):

    response = client.delete(
        f'/api/home_page_api/remove_tool/{sample_home_page_tool.id}',
    )
    assert response.status_code == 200

def test_get_update_tool(db_session,client,sample_home_page_tool):
    response = client.get(
        f'/api/home_page_api/get_by_id/{sample_home_page_tool.id}',
    )
    assert response.status_code == 200

def test_update_tool(db_session,client,sample_home_page_tool):
    data = {
        "id":1,
        "name":"ghk-test1",
        "category_id":"1",
        "category_name":"test",
        "description":"测试调用",
        "url":"aaa",
        "favorites":3,
        "image_url":"bbb",
        "icon_url":"ccc",
        "tags":"fff"}
    response = client.put(
        f'/api/home_page_api/update_tool',
        json=data
    )
    assert response.status_code == 200