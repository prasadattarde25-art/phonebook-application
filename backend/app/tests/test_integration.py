from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_and_get_contact_integration():
    contact = {
        "name": "Integration Test",
        "phone_number": "9000000001",
        "email": "integration@test.com",
        "address": "Mumbai"
    }

    # Create contact
    create_response = client.post(
        "/contacts/",
        json=contact
    )

    assert create_response.status_code == 200

    created_contact = create_response.json()

    assert created_contact["name"] == "Integration Test"
    assert created_contact["phone_number"] == "9000000001"

    contact_id = created_contact["id"]

    # Get the same contact
    get_response = client.get(
        f"/contacts/{contact_id}"
    )

    assert get_response.status_code == 200

    fetched_contact = get_response.json()

    assert fetched_contact["id"] == contact_id
    assert fetched_contact["name"] == "Integration Test"
    assert fetched_contact["email"] == "integration@test.com"

    # Cleanup
    delete_response = client.delete(
        f"/contacts/{contact_id}"
    )

    assert delete_response.status_code == 200