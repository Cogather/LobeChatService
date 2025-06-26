
def test_user_access_data_db(db_session,client):
    data = {
        "user_name":"test1",
        "access_platform":"access_platform"
    }

    response = client.post("/api/user_access", json=data)
    assert response.status_code == 200