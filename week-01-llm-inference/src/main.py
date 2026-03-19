"""
FastAPI application entry point for LLM inference service.

This module implements a layered architecture:
- API Layer: Request handling, authentication, rate limiting
- Business Logic: Inference management, response formatting
- Model Layer: vLLM server communication
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import time
from typing import Optional

from .api.routes import router
from .api.auth import get_api_key
from .core.config import settings
from .monitoring.metrics import (
    request_counter,
    request_duration,
    active_requests,
    error_counter
)

# Initialize FastAPI app
app = FastAPI(
    title="Andromeda LLM Inference API",
    description="Production-grade LLM inference service with monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include API routes
app.include_router(router, prefix="/v1", tags=["inference"])


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    """
    Middleware to track request metrics.
    
    Records:
    - Request count by endpoint and status code
    - Request duration (histogram)
    - Active requests (gauge)
    - Error count
    """
    start_time = time.time()
    active_requests.inc()
    
    try:
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        request_counter.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        if response.status_code >= 400:
            error_counter.labels(
                endpoint=request.url.path,
                error_type=f"HTTP_{response.status_code}"
            ).inc()
        
        return response
    
    except Exception as e:
        error_counter.labels(
            endpoint=request.url.path,
            error_type=type(e).__name__
        ).inc()
        raise
    
    finally:
        active_requests.dec()


@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancers.
    
    Returns:
        dict: Status and version info
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "model": settings.MODEL_NAME
    }


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "service": "Andromeda LLM Inference API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
