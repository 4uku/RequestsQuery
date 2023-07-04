from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)
JSON = {
    "urls": [
        {"url": "https://pyth7on.org", "query": "python"},    
        {"url": "https://www.djangoproject.com", "query": "django"},
        {"url": "https://sanic.dev/en/", "query": "python"},
    ],  
    "max_timeout": 5
}

def test_counts():
    response = client.post('/counts/', json=JSON)
    assert response.status_code == 200
    # для ожидаемого результат я подсчитал количество слов в теле ответа
    # с помощью cURL:
    # curl -s https://docs.pytest.org/en/7.3.x/contents.html | grep -o 'pytest' | wc -l
    assert response.json() == {
        'urls': [
            {'url': 'https://pyth7on.org', 'status': 'error'},
            {'url': 'https://www.djangoproject.com', 'count': 99, 'status': 'ok'},
            {'url': 'https://sanic.dev/en/', 'count': 24, 'status': 'ok'}
        ]
    }