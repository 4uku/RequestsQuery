from secrets import token_hex

import pytest
from httpx import AsyncClient

from src.utils import count_query, fetch


@pytest.mark.asyncio
async def test_available_url_fetch():
    """
    Тестирование запроса к доступной ссылке.
    """
    url = 'https://ya.ru'
    timeout = 1
    async with AsyncClient() as client:
        response = await fetch(url=url, client=client, timeout=timeout)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_unavailable_url_fetch():
    """
    Тестирование запроса к недоступной ссылке.
    """
    url = f'https://{token_hex(8)}.ru'
    timeout = 1
    async with AsyncClient() as client:
        response = await fetch(url=url, client=client, timeout=timeout)
    assert response is None

@pytest.mark.asyncio
async def test_timeout_fetch():
    """
    Тестирование запроса с ограничением по таймауту.
    """
    url = 'https://ya.ru'
    timeout = 0.001
    async with AsyncClient() as client:
        response = await fetch(url=url, client=client, timeout=timeout)
    assert response is None

@pytest.mark.asyncio
async def test_count_query():
    '''
    Тестирование функции подсчета количества вхождений слова в тело ответа.

    Наверное, этот тест стоило разбить на несколько мелких.
    '''
    random_url = f'https://{token_hex(8)}.ru' 
    urls = [
        {
            'url': 'https://docs.pytest.org/en/7.3.x/contents.html',
            'query': 'pytest'
        },
        {
            'url': 'https://docs.pytest.org/en/7.3.x/contents.html',
            'query': 'assert'
        },
        {
            'url': 'https://docs.pytest.org/en/7.3.x/contents.html',
            'query': 'молоко'
        },
        {
            'url': random_url,
            'query': 'бананы'
        }
    ]
    timeout = 1
    result = await count_query(urls=urls, timeout=timeout)

    # для ожидаемого результат я подсчитал количество слов в теле ответа
    # с помощью cURL:
    # curl -s https://docs.pytest.org/en/7.3.x/contents.html | grep -o 'pytest' | wc -l
    assert result == [
        {
            'url': 'https://docs.pytest.org/en/7.3.x/contents.html',
            'count': 75,
            'status': 'ok'
        }, 
        {
            'url': 'https://docs.pytest.org/en/7.3.x/contents.html',
            'count': 20,
            'status': 'ok'
        },
        {
            'url': 'https://docs.pytest.org/en/7.3.x/contents.html',
            'count': 0,
            'status': 'ok'
        },
        {
            'url': random_url,
            'status': 'error'
        }
    ]