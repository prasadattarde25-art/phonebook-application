from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_contact():
    return {
        "name": "Test Rahul",
        "phone_number": "9876543210",
        "email": "testrahul@example.com",
        "address": "Mumbai"
    }


# --------------------------------------------------
# 1. CREATE CONTACT
# --------------------------------------------------

def test_create_contact():
    response = client.post(
        "/contacts/",
        json=create_test_contact()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Rahul"
    assert data["phone_number"] == "9876543210"

    # Cleanup
    contact_id = data["id"]

    client.delete(f"/contacts/{contact_id}")


# --------------------------------------------------
# 2. GET CONTACTS
# --------------------------------------------------

def test_get_contacts():
    response = client.get("/contacts/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "pages" in data

    assert isinstance(data["items"], list)


# --------------------------------------------------
# 3. SEARCH CONTACT
# --------------------------------------------------

def test_search_contact():
    contact = create_test_contact()

    create_response = client.post(
        "/contacts/",
        json=contact
    )

    assert create_response.status_code == 200

    contact_id = create_response.json()["id"]

    response = client.get(
        "/contacts/",
        params={"search": "Test Rahul"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    names = [
        item["name"]
        for item in data["items"]
    ]

    assert "Test Rahul" in names

    # Cleanup
    client.delete(f"/contacts/{contact_id}")


# --------------------------------------------------
# 4. PAGINATION
# --------------------------------------------------

def test_pagination():
    response = client.get(
        "/contacts/",
        params={
            "page": 1,
            "limit": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["items"]) <= 10


# --------------------------------------------------
# 5. GET SINGLE CONTACT
# --------------------------------------------------

def test_get_single_contact():
    contact = create_test_contact()

    create_response = client.post(
        "/contacts/",
        json=contact
    )

    assert create_response.status_code == 200

    contact_id = create_response.json()["id"]

    response = client.get(
        f"/contacts/{contact_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == contact_id
    assert data["name"] == "Test Rahul"

    # Cleanup
    client.delete(f"/contacts/{contact_id}")


# --------------------------------------------------
# 6. UPDATE CONTACT
# --------------------------------------------------

def test_update_contact():
    contact = create_test_contact()

    create_response = client.post(
        "/contacts/",
        json=contact
    )

    assert create_response.status_code == 200

    contact_id = create_response.json()["id"]

    updated_data = {
        "name": "Updated Rahul",
        "phone_number": "9876543210",
        "email": "updatedrahul@example.com",
        "address": "Pune"
    }

    response = client.put(
        f"/contacts/{contact_id}",
        json=updated_data
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Rahul"
    assert data["email"] == "updatedrahul@example.com"
    assert data["address"] == "Pune"

    # Cleanup
    client.delete(f"/contacts/{contact_id}")


# --------------------------------------------------
# 7. DELETE CONTACT
# --------------------------------------------------

def test_delete_contact():
    contact = create_test_contact()

    create_response = client.post(
        "/contacts/",
        json=contact
    )

    assert create_response.status_code == 200

    contact_id = create_response.json()["id"]

    response = client.delete(
        f"/contacts/{contact_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Contact deleted successfully"

    # Verify contact no longer exists
    get_response = client.get(
        f"/contacts/{contact_id}"
    )

    assert get_response.status_code == 404


# --------------------------------------------------
# 8. DUPLICATE PHONE VALIDATION
# --------------------------------------------------

def test_duplicate_phone():
    contact = create_test_contact()

    first_response = client.post(
        "/contacts/",
        json=contact
    )

    assert first_response.status_code == 200

    contact_id = first_response.json()["id"]

    duplicate_contact = {
        "name": "Another Rahul",
        "phone_number": "9876543210",
        "email": "another@example.com",
        "address": "Mumbai"
    }

    response = client.post(
        "/contacts/",
        json=duplicate_contact
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Phone number already exists"

    # Cleanup
    client.delete(f"/contacts/{contact_id}")