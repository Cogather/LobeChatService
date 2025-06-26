from models.news_catalog import Catalog


def test_get_catalog_news_list(client,sample_catalog,mocker):
    result = Catalog(value=1,label=1,title=1)
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [result]
    # 关键修改：让json()方法返回一个可序列化的字典而不是MagicMock对象
    mock_response.json.return_value = {"status": "success"}
    mock_post = mocker.patch('models.news_catalog.Catalog.query', return_value=mock_response)
    response = client.get(
        '/api/news_api/get_catalog_list'
    )
    assert response.status_code == 200

def test_get_news_list(client,sample_catalog,sample_news):
    response = client.get(
        f'/api/news_api/get_news_list/{sample_catalog.catalog_id}'
    )
    assert response.status_code == 200

def test_add_news_catalog(db_session,client):
    data = {
        "value":"aa",
        "label":"label",
        "title":"title"
    }
    datas = []
    datas.append(data)
    response = client.post(
        f'/api/news_api/add_news_catalog',
        json = datas
    )
    assert response.status_code == 200

def test_add_news(db_session,client,sample_catalog):
    data = {
        "value":"1",
        "sectionData":"sectionData",
        "anotherData":"anotherData"
    }
    datas = []
    datas.append(data)
    response = client.post(
        f'/api/news_api/add_news',
        json = datas
    )
    assert response.status_code == 200

