"""
API key authentication and rate limiting.
"""

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Rate limiting storage (in-memory, use Redis in production)
rate_limit_storage: Dict[str, list] = defaultdict(list)


def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Verify API key from Authorization header.
    
    Args:
        credentials: HTTP Bearer token
    
    Returns:
        str: Validated API key
    
    Raises:
        HTTPException: If API key is invalid
    """
    api_key = credentials.credentials
    valid_keys = settings.get_api_keys()
    
    if api_key not in valid_keys:
        logger.warning(f"Invalid API key attempt: {api_key[:8]}...")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return api_key


def check_rate_limit(api_key: str) -> bool:
    """
    Check if API key has exceeded rate limit.
    
    Rate limit: RATE_LIMIT_PER_MINUTE requests per minute per key.
    
    Args:
        api_key: API key to check
    
    Returns:
        bool: True if within limit, False if exceeded
    """
    now = datetime.now()
    one_minute_ago = now - timedelta(minutes=1)
    
    # Get recent requests for this key
    recent_requests = rate_limit_storage[api_key]
    
    # Filter requests within the last minute
    recent_requests = [
        req_time for req_time in recent_requests
        if req_time > one_minute_ago
    ]
    
    # Update storage
    rate_limit_storage[api_key] = recent_requests
    
    # Check limit
    if len(recent_requests) >= settings.RATE_LIMIT_PER_MINUTE:
        logger.warning(
            f"Rate limit exceeded for key: {api_key[:8]}... "
            f"({len(recent_requests)} requests in last minute)"
        )
        return False
    
    # Add current request
    rate_limit_storage[api_key].append(now)
    return True


def get_rate_limit_status(api_key: str) -> dict:
    """
    Get current rate limit status for API key.
    
    Returns:
        dict: Rate limit info (used, limit, reset_time)
    """
    now = datetime.now()
    one_minute_ago = now - timedelta(minutes=1)
    
    recent_requests = [
        req_time for req_time in rate_limit_storage.get(api_key, [])
        if req_time > one_minute_ago
    ]
    
    remaining = max(0, settings.RATE_LIMIT_PER_MINUTE - len(recent_requests))
    
    return {
        "limit": settings.RATE_LIMIT_PER_MINUTE,
        "used": len(recent_requests),
        "remaining": remaining,
        "reset_at": (now + timedelta(minutes=1)).isoformat()
    }
