import logging

from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRouter

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Core TMF Platform",
    description="Core Platform acting as proxy to legacy systems",
    version="1.0.0",
)


# Health endpoint
@app.get(
    "/health",
    summary="Health Check",
    description="Simple health check endpoint",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Service is healthy",
            "content": {"text/plain": {"example": "OK"}},
        }
    },
)
async def health_check() -> str:
    return "OK"


# Initialize the router for product catalog functionality
# Will be populated in later milestones
catalog_router = APIRouter(prefix="/tmf-api/productCatalogManagement/v5")
app.include_router(catalog_router)
