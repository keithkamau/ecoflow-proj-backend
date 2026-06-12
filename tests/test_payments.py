def test_get_payments(client):
    response = client.get("/api/v1/payments/")
    assert response.status_code == 200


def test_payment_not_found(client):
    response = client.get("/api/v1/payments/99999")
    assert response.status_code == 404


def test_create_payment_invalid_transaction(client):
    response = client.post("/api/v1/payments/", json={
        "transaction_id": 99999,
        "user_id": 1,
        "amount": 500.0,
        "payment_method": "mpesa"
    })
    assert response.status_code == 404
