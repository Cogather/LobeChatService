def test_update_user_group(client,sample_user_link):
    data = {
        "applicant":"test_name",
        "modify_group":"2",
        "approval_comments":"111"
    }
    response = client.post("/api/user_group_api/update_group",json=data)
    assert response.status_code == 200

def test_remove_user_group(client,sample_user_link):
    data = {
        "applicant":"test_name",
        "modify_group":"2",
        "approval_comments":"111"
    }
    response = client.post("/api/user_group_api/remove_group",json=data)
    assert response.status_code == 200

def test_approval_permission_change(client,sample_user_link,sample_group_permission_records):
    data = {
        "approved_by":"test_name",
        "approval_comments":"2"
    }
    response = client.post(f"/api/user_group_api/approval_permission/{sample_group_permission_records.id}",json=data)
    assert response.status_code == 200