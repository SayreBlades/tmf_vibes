"""Main FastAPI application for the mock legacy platform."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query, Response, status

# Import JSONResponse
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# Import the loaded data using the package path
from some_legacy_platform.data_loader import PRODUCT_OFFERINGS_DB

# Import both models
from some_legacy_platform.models import ProductOffering, ProductOfferingPartial

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
    version="1.0.0",
    lifespan=lifespan,
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


# --- Product Offering Endpoints ---


@app.get(
    "/productOffering/{offering_id}",
    # Use the Partial model for the response_model
    response_model=ProductOfferingPartial,
    summary="Retrieve a single Product Offering by ID",
    description="Retrieves the details of a specific product offering, optionally allowing field selection.",
    tags=["Product Offering"],
    responses={
        status.HTTP_200_OK: {
            "description": "Successful retrieval of product offering (potentially partial based on 'fields' query parameter)",
            # Explicitly document the partial model here
            "model": ProductOfferingPartial,
            "content": {
                "application/json": {
                    "examples": {
                        "full_offering": {
                            "summary": "Full Offering Example",
                            "value": {
                                "id": "offer001",
                                "href": "/productOffering/offer001",
                                "name": "Basic Broadband 50",
                                "description": "Standard home broadband package with 50 Mbps download speed.",
                                "version": "1.0",
                                "isBundle": False,
                                "isSellable": True,
                                "lifecycleStatus": "Active",
                                "lastUpdate": "2023-10-26T10:00:00Z",
                                "@type": "ProductOffering",
                                "@baseType": "ProductOffering",
                            },
                        },
                        "partial_offering": {
                            "summary": "Partial Offering Example (fields=id,name)",
                            "value": {
                                "id": "offer001",
                                "name": "Basic Broadband 50",
                            },
                        },
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request - Invalid field(s) requested",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid fields requested: ['invalidField']"}
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Product Offering not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Product Offering with id '...' not found"}
                }
            },
        },
    },
)
async def get_product_offering(
    offering_id: str,
    fields: Optional[str] = Query(
        default=None,
        description="Comma-separated list of top-level fields to return.",
        examples=["id,name,description,@type"],
    ),
) -> Any:  # Return Any because it could be a model or a dict or JSONResponse
    """
    Retrieve a Product Offering by its ID.

    Supports field selection via the `fields` query parameter.
    """
    logger.info(
        f"Received request for product offering ID: {offering_id} with fields: {fields}"
    )

    offering_data = product_offerings_store.get(offering_id)
    if not offering_data:
        logger.warning(f"Product offering with ID '{offering_id}' not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product Offering with id '{offering_id}' not found",
        )

    try:
        # Validate and parse the data using the STRICT Pydantic model
        offering_model = ProductOffering(**offering_data)
    except ValidationError as e:
        logger.error(
            f"Data validation error for offering ID '{offering_id}': {e}",
            exc_info=True,
        )
        # This indicates an internal data problem, hence 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Data inconsistency for offering ID '{offering_id}'.",
        ) from e

    if not fields:
        # No field selection requested, return the full validated model instance
        # FastAPI will validate this against ProductOfferingPartial (which will pass)
        logger.debug(f"Returning full model for offering ID: {offering_id}")
        return offering_model

    # --- Field Selection Logic ---
    requested_fields_set = {
        f.strip() for f in fields.split(",") if f.strip()
    }
    if not requested_fields_set:
        # Fields parameter was present but empty, return full model instance
        logger.debug(
            f"Empty 'fields' parameter, returning full model for offering ID: {offering_id}"
        )
        return offering_model

    # Get valid field names/aliases as they appear in JSON schema
    # Use the PARTIAL model here to get the list of valid keys for filtering
    valid_json_keys = set(
        ProductOfferingPartial.model_json_schema(by_alias=True)[
            'properties'
        ].keys()
    )

    # Check for invalid requested fields
    invalid_fields = requested_fields_set - valid_json_keys
    if invalid_fields:
        logger.warning(
            f"Invalid fields requested for offering ID '{offering_id}': {invalid_fields}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid fields requested: {sorted(list(invalid_fields))}",
        )

    # Dump the STRICT model to a dict using aliases, then filter
    full_dict = offering_model.model_dump(by_alias=True)
    filtered_dict = {
        key: value
        for key, value in full_dict.items()
        if key in requested_fields_set
    }

    logger.debug(
        f"Returning filtered fields {requested_fields_set} for offering ID: {offering_id}"
    )
    # Return the filtered dictionary explicitly wrapped in a JSONResponse
    # This bypasses FastAPI's response_model processing for this path
    return JSONResponse(content=filtered_dict)
