
def test_operation_data(client,db_session,sample_user_access):
    response =client.get("/api/operation_api/home_page_or_chat")
    assert response.status_code == 200

def test_active_users(client,db_session,sample_user_access):
    response =client.get("/api/operation_api/home_page_or_chat")
    assert response.status_code == 200

def test_active_users_operation_data(client,db_session,sample_message):
    data = {"start_time":"2025-05-01","end_time":"2025-06-01"}
    response =client.post("/api/operation_api/active_users",json=data)
    assert response.status_code == 200

def test_active_users_operation_trend(client,db_session,sample_message):
    data = {"start_time":"2025-05-01","end_time":"2025-06-01","date_type":"month"}
    response =client.post("/api/operation_api/active_users_trend",json=data)

    data1 = {"start_time":"2025-05-01","end_time":"2025-06-01","date_type":"week"}
    response1 =client.post("/api/operation_api/active_users_trend",json=data1)
    assert response.status_code == 200
    assert response1.status_code == 200

def test_operation_permission(client,db_session,sample_user_link):
    response =client.post(f"/api/operation_api/operation_permission/{sample_user_link.user_name}")
    assert response.status_code == 200

def test_export_to_excel(client,db_session,sample_message,sample_user_info_tool):
    response =client.post("/api/operation_api/export_to_excel")
    assert response.status_code == 200