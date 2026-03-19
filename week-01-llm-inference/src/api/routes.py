"""
API routes for LLM inference endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from ..api.auth import verify_api_key, check_rate_limit
from ..core.inference import InferenceManager

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize inference manager
inference_manager = InferenceManager()


class Message(BaseModel):
    """Chat message schema."""
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat completion request schema."""
    messages: List[Message] = Field(..., description="List of chat messages")
    model: Optional[str] = Field(None, description="Model to use (optional)")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(2048, ge=1, le=4096, description="Maximum tokens to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream responses")


class ChatResponse(BaseModel):
    """Chat completion response schema."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[dict]
    usage: dict


@router.post("/chat/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate chat completion using LLM.
    
    Requires valid API key in Authorization header:
    `Authorization: Bearer YOUR_API_KEY`
    
    Rate limit: 10 requests per minute per API key.
    """
    # Check rate limit
    if not check_rate_limit(api_key):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Maximum 10 requests per minute."
        )
    
    try:
        # Call inference manager
        response = await inference_manager.generate(
            messages=[msg.dict() for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {str(e)}"
        )


@router.get("/models")
async def list_models(api_key: str = Depends(verify_api_key)):
    """
    List available models.
    
    Returns information about models available for inference.
    """
    return {
        "object": "list",
        "data": [
            {
                "id": "Qwen/Qwen2.5-7B-Instruct",
                "object": "model",
                "owned_by": "Qwen",
                "permission": []
            }
        ]
    }
