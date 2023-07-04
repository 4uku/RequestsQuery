import asyncio
from typing import Optional

from fake_headers import Headers
from httpx import AsyncClient, Response


async def fetch(
        url: str, client: AsyncClient, timeout: int) -> Optional[Response]:
    headers = Headers(headers=False).generate()
    try:
        response = await client.get(
            url=url,
            headers=headers,
            timeout=timeout,
            follow_redirects=True
        )
        return response
    except:
        return None


async def count_query(
        urls: list[dict[str, str]], timeout: int) -> list[dict[str, str]]:
    async with AsyncClient() as client:
        responses = await asyncio.gather(
            *[fetch(url.get('url'), client, timeout) for url in urls]
        )
    
    for url, response in zip(urls, responses):
        query = url.pop('query')

        if response and response.status_code == 200:
            query_count = response.text.count(query)
            url.update({'count': query_count, 'status': 'ok'})
        else:
            url.update({'status': 'error'})
    
    return urls
