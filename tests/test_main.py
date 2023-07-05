from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_counts(mocker):
    json = {
        "urls": [
            {"url": "http://test_url_1.test", "query": "python"},    
            {"url": "https://test_url_2.test", "query": "django"}
        ],
        "max_timeout": 3000
    }
    expected = {
        'urls': [
            {'url': 'http://test_url_1.test', 'count': 1, 'status': 'ok'},
            {'url': 'http://test_url_2.test', 'status': 'error'}
        ]
    }
    mock_return_value = [
        {'url': 'http://test_url_1.test', 'count': 1, 'status': 'ok'},
        {'url': 'http://test_url_2.test', 'status': 'error'}
    ]

    mocker.patch('src.main.count_query', return_value=mock_return_value)
    response = client.post('/counts/', json=json)
    assert response.status_code == 200
    assert response.json() == expected
