"""Loads static product offering data from JSON files."""

import json
import logging
from pathlib import Path
from typing import Any  # Dict removed

logger = logging.getLogger(__name__)

# Determine the project root relative to this file
# src/some_legacy_platform/data_loader.py -> src/some_legacy_platform/ -> src/
# -> project root (some_legacy_platform)
SRC_ROOT = Path(__file__).parent.parent
PROJECT_ROOT = SRC_ROOT.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_product_offerings() -> dict[str, dict[str, Any]]:
    """
    Loads product offering JSON files from the data directory.

    Returns:
        A dictionary where keys are offering IDs and values are the
        loaded product offering dictionaries.
    """
    offerings: dict[str, dict[str, Any]] = {}
    if not DATA_DIR.is_dir():
        logger.error(f"Data directory not found: {DATA_DIR}")
        return offerings

    logger.info(f"Loading product offerings from: {DATA_DIR}")
    file_count = 0
    for file_path in DATA_DIR.glob("*.json"):
        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                offering_id = data.get("id")
                if offering_id:
                    offerings[offering_id] = data
                    file_count += 1
                    logger.debug(
                        f"Loaded offering '{offering_id}' from {file_path.name}"
                    )
                else:
                    logger.warning(
                        f"Skipping file {file_path.name}: missing 'id' field."
                    )
        except json.JSONDecodeError:
            logger.error(
                f"Error decoding JSON from file: {file_path.name}", exc_info=True
            )
        except Exception:
            logger.error(f"Error loading file: {file_path.name}", exc_info=True)

    logger.info(f"Successfully loaded {file_count} product offerings.")
    return offerings


# Load data immediately when the module is imported.
# This acts as a simple cache.
PRODUCT_OFFERINGS_DB: dict[str, dict[str, Any]] = load_product_offerings()
