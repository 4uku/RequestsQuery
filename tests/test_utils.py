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
    async def test_count_query_with_all_data(self, httpx_mock: HTTPXMock):
        """
        Тестирование функции count_query с заведомо присутствующими словамми.
        Результат должен содержать ссылку, количество найденных слов и
        статус 'ok.
        """
        expect = [{'url': 'http://test_url', 'count': 3, 'status': 'ok'}]
        urls = [
            {'url': 'http://test_url', 'query': 'python'}]

        httpx_mock.add_response(text='python python python')
        async with AsyncClient() as client: # ruff: noqa: F841
            result = await count_query(urls, timeout=1)
            assert result == expect

    @pytest.mark.asyncio
    async def test_count_query_with_zero(self, httpx_mock: HTTPXMock):
        """
        Тестирование функции count_query. Результат должен содержать ссылку,
        ноль найденных слов и статус 'ok'.
        """
        expect = [{'url': 'http://test_url', 'count': 0, 'status': 'ok'}]
        urls = [
            {'url': 'http://test_url', 'query': 'python'}]

        httpx_mock.add_response(text='wrong')
        async with AsyncClient() as client: # ruff: noqa: F841
            result = await count_query(urls, timeout=1)
            assert result == expect

    @pytest.mark.asyncio
    async def test_count_query_with_status_error(self, httpx_mock: HTTPXMock):
        """
        Тестирование функции count_query. Результат должен содержать ссылку,
        и статус 'error'.
        """
        expect = [{'url': 'http://test_url', 'status': 'error'}]
        urls = [
            {'url': 'http://test_url', 'query': 'python'}]

        httpx_mock.add_exception(TimeoutException('timeout_error'))
        async with AsyncClient() as client: # ruff: noqa: F841
            result = await count_query(urls, timeout=1)
            assert result == expect
