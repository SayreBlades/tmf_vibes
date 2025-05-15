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


# --- Tests for GET /productOffering (List) ---

TOTAL_OFFERINGS = len(VALID_OFFERING_IDS) # Should be 10


def test_list_product_offerings_default_pagination() -> None:
    """Test listing with default offset (0) and limit (10)."""
    response = client.get("/productOffering")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == min(TOTAL_OFFERINGS, 10)  # Default limit is 10
    if data:
        # Check structure of the first item (should be full, as per ProductOfferingPartial)
        assert "id" in data[0]
        assert "name" in data[0]
        assert "@type" in data[0]
        assert "lastUpdate" in data[0]


def test_list_product_offerings_custom_limit() -> None:
    """Test listing with a custom limit."""
    limit = 2
    response = client.get(f"/productOffering?limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == limit
    if data:
        assert data[0]["id"] == VALID_OFFERING_IDS[0] # Assuming sorted by ID
        assert data[1]["id"] == VALID_OFFERING_IDS[1]


def test_list_product_offerings_custom_offset() -> None:
    """Test listing with a custom offset."""
    offset = 2
    response = client.get(f"/productOffering?offset={offset}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    # Default limit is 10, so TOTAL_OFFERINGS - offset items, or 0 if offset is too large
    expected_len = max(0, min(TOTAL_OFFERINGS - offset, 10))
    assert len(data) == expected_len
    if data:
        assert data[0]["id"] == VALID_OFFERING_IDS[offset] # Assuming sorted by ID


def test_list_product_offerings_offset_and_limit() -> None:
    """Test listing with both offset and limit."""
    offset = 1
    limit = 3
    response = client.get(f"/productOffering?offset={offset}&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == limit
    if data:
        assert data[0]["id"] == VALID_OFFERING_IDS[offset]
        assert data[1]["id"] == VALID_OFFERING_IDS[offset + 1]
        assert data[2]["id"] == VALID_OFFERING_IDS[offset + 2]


def test_list_product_offerings_offset_out_of_bounds() -> None:
    """Test listing with an offset greater than the number of items."""
    offset = TOTAL_OFFERINGS + 5
    response = client.get(f"/productOffering?offset={offset}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_list_product_offerings_limit_exceeds_available() -> None:
    """Test listing with a limit that exceeds available items after offset."""
    offset = TOTAL_OFFERINGS - 2 # e.g., offset 8 for 10 items
    limit = 5 # Request 5, but only 2 are available
    response = client.get(f"/productOffering?offset={offset}&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == TOTAL_OFFERINGS - offset # Should be 2
    if data:
        assert data[0]["id"] == VALID_OFFERING_IDS[offset]


def test_list_product_offerings_with_fields_selection() -> None:
    """Test listing with field selection."""
    fields_to_request = "id,name,@type"
    response = client.get(f"/productOffering?fields={fields_to_request}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == min(TOTAL_OFFERINGS, 10) # Default limit
    if data:
        item = data[0]
        expected_keys = sorted(fields_to_request.split(","))
        assert sorted(list(item.keys())) == expected_keys
        assert "id" in item
        assert "name" in item
        assert "@type" in item
        assert "description" not in item


def test_list_product_offerings_pagination_and_fields() -> None:
    """Test listing combining pagination and field selection."""
    offset = 1
    limit = 2
    fields_to_request = "href,version"
    response = client.get(
        f"/productOffering?offset={offset}&limit={limit}&fields={fields_to_request}"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == limit
    if data:
        for item in data:
            expected_keys = sorted(fields_to_request.split(","))
            assert sorted(list(item.keys())) == expected_keys
            assert "href" in item
            assert "version" in item
            assert "id" not in item
        assert data[0]["href"] == f"/productOffering/{VALID_OFFERING_IDS[offset]}"
        assert data[1]["href"] == f"/productOffering/{VALID_OFFERING_IDS[offset+1]}"


def test_list_product_offerings_with_invalid_fields() -> None:
    """Test listing with an invalid field name."""
    fields_to_request = "id,name,nonExistentField"
    response = client.get(f"/productOffering?fields={fields_to_request}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error_data = response.json()
    assert "detail" in error_data
    assert "nonExistentField" in error_data["detail"]


def test_list_product_offerings_empty_fields_parameter() -> None:
    """Test listing with an empty fields parameter (should return all fields)."""
    response = client.get("/productOffering?fields=")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == min(TOTAL_OFFERINGS, 10)
    if data:
        # Check if it returns more than just one or two fields (heuristic for 'all')
        assert len(data[0].keys()) > 2
        assert "id" in data[0]
        assert "name" in data[0]
        assert "description" in data[0] # Example of a field that might be excluded by specific selection


def test_list_product_offerings_invalid_offset_negative() -> None:
    """Test listing with negative offset."""
    response = client.get("/productOffering?offset=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_product_offerings_invalid_limit_zero() -> None:
    """Test listing with limit=0."""
    response = client.get("/productOffering?limit=0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_product_offerings_invalid_limit_negative() -> None:
    """Test listing with negative limit."""
    response = client.get("/productOffering?limit=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_product_offerings_limit_too_large() -> None:
    """Test listing with limit greater than max allowed (100)."""
    response = client.get("/productOffering?limit=101")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

