from fastapi import FastAPI
from fastapi.testclient import TestClient

from portal.modules.data.router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_data():
    """test data"""

    response = client.post("/data")
    assert response.status_code == 200
