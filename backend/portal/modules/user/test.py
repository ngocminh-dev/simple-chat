"""Test user router"""
from unittest import mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from portal.modules.user.router import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


@mock.patch("portal.modules.core.security.validate_token")
def test_me(mock_validate_token: mock.Mock):
    """test"""
    res = {"id": "id", "fullname": "mail@a.b", "email": "mail@a.b"}
    mock_validate_token.return_value = {
        "sub": res["email"],
        "uid": res["id"],
    }

    response = client.get("/me", headers={"Authorization": "Bearer token"})
    mock_validate_token.assert_called_once()
    assert response.json() == res
    assert response.status_code == 200


def product(a: float, b: float, c: float, d: float) -> float:
    """product"""
    return a * b * c * d


@mock.patch("portal.modules.employee.schema.EmployeeModel.save")
def test_function(mock_save: mock.Mock):
    """test function"""

    mock_save.return_value = {}  # mock employee
    assert product(1, 2, 3, 4) == 24
    mock_save.assert_called_once_with({"salary": 24})  # update employee paylod


def test_function_fail():
    """test function fail"""
    assert product(1, 2, 3, 4) != 23
