import time


def get_token(client):
    email = f"test{time.time()}@gmail.com"

    client.post("/auth/register", json={
        "email": email,
        "password": "123456"
    })

    res = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "123456"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    return res.json()["access_token"]


# ✅ 1. Create product (authorized)
def test_create_product(client):
    token = get_token(client)

    res = client.post("/products/", json={
        "name": "Laptop",
        "category_id": None
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 201


# ✅ 2. Create product without auth
def test_create_product_no_auth(client):
    res = client.post("/products/", json={
        "name": "Phone",
        "category_id": None
    })

    assert res.status_code == 401


# ✅ 3. Get all products
def test_get_products(client):
    res = client.get("/products/")
    assert res.status_code == 200


# ✅ 4. Get product by id
def test_product_by_id(client):
    token = get_token(client)

    create = client.post("/products/", json={
        "name": "Tablet",
        "category_id": None
    }, headers={"Authorization": f"Bearer {token}"})

    product_id = create.json()["id"]

    res = client.get(f"/products/{product_id}")
    assert res.status_code == 200


# ✅ 5. Invalid product id
def test_product_invalid_id(client):
    res = client.get("/products/999")
    assert res.status_code == 404


# ✅ 6. Update product (authorized)
def test_update_product(client):
    token = get_token(client)

    create = client.post("/products/", json={
        "name": "Old",
        "category_id": None
    }, headers={"Authorization": f"Bearer {token}"})

    pid = create.json()["id"]

    res = client.put(f"/products/{pid}", json={
        "name": "Updated",
        "category_id": None
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200


# ✅ 7. Update product without auth
def test_update_product_no_auth(client):
    res = client.put("/products/1", json={
        "name": "Fail",
        "category_id": None
    })

    assert res.status_code == 401


# ✅ 8. Delete product (authorized)
def test_delete_product(client):
    token = get_token(client)

    create = client.post("/products/", json={
        "name": "DeleteMe",
        "category_id": None
    }, headers={"Authorization": f"Bearer {token}"})

    pid = create.json()["id"]

    res = client.delete(f"/products/{pid}", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200


# ✅ 9. Delete product without auth
def test_delete_product_no_auth(client):
    res = client.delete("/products/1")
    assert res.status_code == 401


# ✅ 10. Create product invalid data
def test_create_product_invalid_data(client):
    token = get_token(client)

    res = client.post("/products/", json={
        "name": 123
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 422


# ✅ 11. Update non-existing product
def test_update_non_existing_product(client):
    token = get_token(client)

    res = client.put("/products/999", json={
        "name": "X",
        "category_id": None
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 404


# ✅ 12. Delete non-existing product
def test_delete_non_existing_product(client):
    token = get_token(client)

    res = client.delete("/products/999", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 404


# 13. Valid Test token
def test_protected_route_valid_token(client):
    token = get_token(client)

    res = client.post(
        "/products/",
        json={"name": "Valid Product", "category_id": None},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201


# 14. Invalid test token
def test_protected_route_invalid_token(client):
    fake_token = "invalidtoken123"

    res = client.post(
        "/products/",
        json={"name": "No Token Product", "category_id": None},
        headers={"Authorization": f"Bearer {fake_token}"}
    )

    assert res.status_code == 401


# 15. Missing Token Test
def test_protected_route_no_token(client):
    res = client.post(
        "/products/",
        json={"name": "No token product", "category_id": None}
    )

    assert res.status_code == 401
