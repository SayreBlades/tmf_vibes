import logging
from fastapi import FastAPI, status, Depends, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.routing import APIRouter
from core_platform.auth import authenticate

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Core TMF Platform",
    description="Core Platform acting as proxy to legacy systems",
    version="1.0.0",
)


# Health endpoint - no authentication
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

# Apply authentication to all other routes
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/health":
        return await call_next(request)
        
    try:
        authenticate(request)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "code": "UNAUTHORIZED",
                "reason": "Invalid credentials",
                "status": e.status_code
            },
            headers=e.headers
        )
    
    return await call_next(request)


# Initialize the router for product catalog functionality
# Will be populated in later milestones
catalog_router = APIRouter(prefix="/tmf-api/productCatalogManagement/v5")
app.include_router(catalog_router)
