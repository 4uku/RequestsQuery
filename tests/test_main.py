from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

async def test_counts():
    pass
