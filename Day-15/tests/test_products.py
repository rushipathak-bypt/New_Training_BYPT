def test_create_product(client, auth_headers):
    response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == 201


def test_get_products(client, auth_headers):
    response = client.get("/products/", headers=auth_headers)
    assert response.status_code == 200


def test_unauthorized_access(client):
    response = client.get("/products/")
    assert response.status_code == 401


def test_get_single_product(client, auth_headers):
    create = client.post(
        "/products/",
        json={"name": "Item", "description": "Desc"},
        headers=auth_headers
    )
    product_id = create.json()["id"]

    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 200


def test_delete_product(client, auth_headers):
    create = client.post(
        "/products/",
        json={"name": "DeleteMe", "description": "Desc"},
        headers=auth_headers
    )
    product_id = create.json()["id"]

    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 200
