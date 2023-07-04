from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

from .utils import count_query

app = FastAPI()


class InData(BaseModel):
    class Query(BaseModel):
        url: HttpUrl
        query: str

    urls: list[Query]
    max_timeout: float


@app.post('/counts/')
async def counts(data: InData):
    data_dict = data.dict()

    urls = data_dict.get('urls')
    timeout = data_dict.get('max_timeout')

    result = await count_query(urls, timeout=timeout)
    return {'urls': result}
