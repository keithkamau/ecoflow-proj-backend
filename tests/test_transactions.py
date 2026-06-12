def test_get_transactions(client):
    response = client.get("/api/v1/transactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_transaction_not_found(client):
    response = client.get("/api/v1/transactions/99999")
    assert response.status_code == 404


def test_create_transaction_without_accepted_offer(client):
    response = client.post("/api/v1/transactions/", json={
        "offer_id": 99999,
        "listing_id": 1,
        "seller_id": 1,
        "recycler_id": 2,
        "agreed_price": 15.0,
        "final_quantity": 50.0,
        "final_price": 750.0
    })
    assert response.status_code == 404
