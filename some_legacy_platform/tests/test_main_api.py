"""Integration tests for the FastAPI application endpoints."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

# Assuming PRODUCT_OFFERINGS_DB is populated correctly on app startup via lifespan
from some_legacy_platform.main import app

# Create a TestClient instance
client = TestClient(app)

# --- Test Data ---
VALID_OFFERING_IDS = [f"offer{i:03d}" for i in range(1, 11)]
NON_EXISTENT_ID = "offer999"


# --- Tests for GET /productOffering/{id} ---


@pytest.mark.parametrize("offering_id", VALID_OFFERING_IDS)
def test_get_product_offering_by_id_success(offering_id: str) -> None:
    """Test retrieving existing product offerings by ID."""
    response = client.get(f"/productOffering/{offering_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == offering_id
    assert "@type" in data
    assert "name" in data
    assert "lastUpdate" in data  # Verify required field is present


def test_get_product_offering_by_id_not_found() -> None:
    """Test retrieving a non-existent product offering ID."""
    response = client.get(f"/productOffering/{NON_EXISTENT_ID}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_product_offering_by_id_fields_selection_valid() -> None:
    """Test retrieving an offering with valid field selection."""
    offering_id = VALID_OFFERING_IDS[0]
    fields_to_request = "id,name,version"
    response = client.get(f"/productOffering/{offering_id}?fields={fields_to_request}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Check keys directly against the requested fields string
    assert sorted(list(data.keys())) == sorted(fields_to_request.split(","))
    assert data["id"] == offering_id
    assert "name" in data
    assert "version" in data
    assert "description" not in data  # Ensure other fields are excluded


def test_get_product_offering_by_id_fields_selection_one_field() -> None:
    """Test retrieving an offering with single field selection."""
    offering_id = VALID_OFFERING_IDS[1]
    fields_to_request = "description"
    response = client.get(f"/productOffering/{offering_id}?fields={fields_to_request}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert list(data.keys()) == [fields_to_request]
    assert "description" in data
    assert "id" not in data


def test_get_product_offering_by_id_fields_selection_with_at_type() -> None:
    """Test retrieving an offering including the @type field."""
    offering_id = VALID_OFFERING_IDS[2]
    # Note: We request '@type' using its alias in the query
    fields_to_request = "id,@type,lifecycleStatus"
    response = client.get(f"/productOffering/{offering_id}?fields={fields_to_request}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # The response keys will use the alias '@type' because we return JSONResponse
    # So, expected keys should match the requested fields directly.
    expected_keys = fields_to_request.split(",")
    assert sorted(list(data.keys())) == sorted(expected_keys)
    assert data["id"] == offering_id
    assert data["@type"] == "ProductOffering" # Check using the alias
    assert "lifecycleStatus" in data


def test_get_product_offering_by_id_fields_selection_invalid_field() -> None:
    """Test retrieving an offering with an invalid field name."""
    offering_id = VALID_OFFERING_IDS[3]
    fields_to_request = "id,name,nonExistentField"
    response = client.get(f"/productOffering/{offering_id}?fields={fields_to_request}")
    # Expecting 400 Bad Request as per user confirmation
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Optionally check the error detail if the API provides one
    # data = response.json()
    # assert "detail" in data
    # assert "nonExistentField" in data["detail"]


def test_get_product_offering_by_id_fields_selection_empty() -> None:
    """Test retrieving an offering with empty fields parameter (should return all)."""
    offering_id = VALID_OFFERING_IDS[4]
    response = client.get(f"/productOffering/{offering_id}?fields=")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Check if it returns more than just one or two fields (heuristic for 'all')
    assert len(data.keys()) > 2
    assert data["id"] == offering_id
    assert "name" in data
    assert "description" in data
    assert "lastUpdate" in data


def test_get_product_offering_by_id_no_fields() -> None:
    """Test retrieving an offering without the fields parameter (should return all)."""
    offering_id = VALID_OFFERING_IDS[5]
    response = client.get(f"/productOffering/{offering_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Check if it returns more than just one or two fields (heuristic for 'all')
    assert len(data.keys()) > 2
    assert data["id"] == offering_id
    assert "name" in data
    assert "description" in data
    assert "lastUpdate" in data
    assert "href" in data
    assert "version" in data
    assert "isBundle" in data
    assert "isSellable" in data
    assert "lifecycleStatus" in data
    assert "@type" in data # Check alias handling in response
    assert "@baseType" in data # Check alias handling in response


# --- Tests for GET /health (already implemented) ---


def test_health_check() -> None:
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "OK"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

