import uuid


def test_register(client):
    email = f"{uuid.uuid4()}@test.com"
    response = client.post("/auth/register", json={
        "email": email,
        "password": "123456"
    })
    assert response.status_code == 200
    assert response.json()["email"] == email


def test_login(client):
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "123456"
    })

    response = client.post("/auth/login", data={
        "username": "login@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
