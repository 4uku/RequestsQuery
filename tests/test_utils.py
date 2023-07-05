from secrets import token_hex

import pytest
from httpx import AsyncClient
from httpx._exceptions import TimeoutException
from pytest_httpx import HTTPXMock

from src.utils import count_query, fetch


class TestFetch():
    @pytest.mark.asyncio
    async def test_available_url_fetch(self, httpx_mock: HTTPXMock):
        """
        Тестирование функции fetch на выполнение запроса.
        """
        httpx_mock.add_response(status_code=200, text='hello')

        async with AsyncClient() as client:
            response = await fetch(url='https://test_url', client=client, timeout=1)
            assert response.status_code == 200
            assert response.text == 'hello'


    @pytest.mark.asyncio
    async def test_timeout_fetch(self, httpx_mock: HTTPXMock):
        """
        Тестирование функции fetch на возврат None при исключении.
        """
        httpx_mock.add_exception(TimeoutException('timeout_error'))

        async with AsyncClient() as client:
            response = await fetch(url='https://test_url', client=client, timeout=1)
            assert response is None


class TestCountQuery():

    @pytest.mark.asyncio
    async def test_count_query(self):
        """
        Тестирование функции подсчета количества вхождений слова в тело ответа.

        Наверное, этот тест стоило разбить на несколько мелких.
        """
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

        """"
        для ожидаемого результат я подсчитал количество слов в теле ответа
        с помощью cURL:
        curl -s https://docs.pytest.org/en/7.3.x/contents.html | 
        grep -o 'pytest' | wc -l
        """
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
