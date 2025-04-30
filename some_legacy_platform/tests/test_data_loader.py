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

    assert len(offerings) == 10
    assert "offer001" in offerings
    assert "offer010" in offerings
    assert offerings["offer001"]["name"] == "Basic Broadband 50"
    assert offerings["offer010"]["name"] == "Gamer Pro Fibre 500"
