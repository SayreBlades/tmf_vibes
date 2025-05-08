"""Tests for the data loading mechanism."""

from some_legacy_platform.data_loader import DATA_DIR, load_product_offerings


def test_load_product_offerings_success() -> None:
    """
    Test successful loading of product offerings from the actual data directory.
    Assumes the 10 JSON files exist in some_legacy_platform/data.
    """
    # Check that the data directory exists
    assert DATA_DIR.is_dir(), f"Data directory not found at {DATA_DIR}"

    offerings = load_product_offerings()

    # Check total count
    assert len(offerings) == 10

    # Check specific offerings are present
    assert "offer001" in offerings
    assert "offer010" in offerings

    # Check specific fields in known offerings
    assert offerings["offer001"]["name"] == "Basic Broadband 50"
    assert offerings["offer010"]["name"] == "Gamer Pro Fibre 500"

    # Check for the newly added required field 'lastUpdate'
    assert "lastUpdate" in offerings["offer001"]
    assert isinstance(offerings["offer001"]["lastUpdate"], str)
    assert offerings["offer001"]["lastUpdate"] == "2023-10-26T10:00:00Z"

    assert "lastUpdate" in offerings["offer010"]
    assert isinstance(offerings["offer010"]["lastUpdate"], str)
    assert offerings["offer010"]["lastUpdate"] == "2024-04-01T09:00:00Z"
