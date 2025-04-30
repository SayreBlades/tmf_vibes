"""Main FastAPI application for the mock legacy platform."""

import logging
from collections.abc import AsyncGenerator  # Dict removed
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Response, status

# Import the loaded data using the package path
from some_legacy_platform.data_loader import PRODUCT_OFFERINGS_DB

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# In-memory storage for loaded data (populated by lifespan)
# We use the pre-loaded data from data_loader directly
product_offerings_store: dict[str, dict[str, Any]] = PRODUCT_OFFERINGS_DB


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    Loads data on startup and can handle cleanup on shutdown.
    """
    logger.info("Application startup: Loading data...")
    # Data is already loaded by data_loader module import
    if not product_offerings_store:
        logger.warning("Product offerings data store is empty after startup!")
    else:
        logger.info(
            f"Loaded {len(product_offerings_store)} product offerings into memory."
        )
    yield
    # Cleanup logic can go here if needed on shutdown
    logger.info("Application shutdown.")


app = FastAPI(
    title="Mock TMF620 Product Catalog",
    description="A mock API simulating a legacy TMF620 Product Catalog system.",
    version="1.0.0",  # Added version from Milestone 1
    lifespan=lifespan,  # Add the lifespan manager
)


@app.get(
    "/health",
    summary="Health Check",
    description="Simple health check endpoint.",
    tags=["Admin"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Service is healthy",
            "content": {"text/plain": {"example": "OK"}},
        }
    },
)
async def health_check() -> Response:
    """Perform a health check."""
    return Response(
        status_code=status.HTTP_200_OK, content="OK", media_type="text/plain"
    )
