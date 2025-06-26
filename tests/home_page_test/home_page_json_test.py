
import pytest

@pytest.fixture
def mock_requests_get(requests_mock):
    def _mock_requests_get(url, status_code, json_data):
        requests_mock.get(url, status_code=status_code, json=json_data)
    return _mock_requests_get





