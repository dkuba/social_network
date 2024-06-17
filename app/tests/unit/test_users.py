import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_user():
    pass


if __name__ == "__main__":
    pytest.main()
