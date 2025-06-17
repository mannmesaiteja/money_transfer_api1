import pytest
from money_tranasfer_api import app
import random



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_transfer(client):
    users = [
        {"sender_id": 2, "receiver_id": 1, "balance": 1000},
        {"sender_id": 1, "receiver_id": 2, "balance": 2000},
        {"sender_id": 3, "receiver_id": 4, "balance": 1500},
        {"sender_id": 4, "receiver_id": 3, "balance": 1800}
    ]
    response = client.post("http://127.0.0.1:5000/transfer", json=random.choice(users))
    assert response.status_code == 200
    assert response.get_json()["message"] == "Transaction is successful"