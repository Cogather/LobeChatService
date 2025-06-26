def test_add_notice(client,sample_user_link):
    data = {
        "user_name":"test_name",
        "notice":"test1",
        "platform_id":1,
        "type":1
    }
    response = client.post("/api/notice_api/add_notice",json=data)
    assert response.status_code == 200

def test_get_latest_notice(client,sample_notice):
    data = {"platform_id":1,"type":"1"}
    response = client.post("/api/notice_api/release_notice",json=data)
    assert response.status_code == 200