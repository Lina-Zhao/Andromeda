"""
Inference manager for communicating with vLLM server.

This module handles:
- Making requests to vLLM OpenAI-compatible API
- Error handling and retries
- Response formatting
"""

import httpx
import time
import logging
from typing import List, Dict, Optional

from .config import settings

logger = logging.getLogger(__name__)


class InferenceManager:
    """Manager for LLM inference operations."""
    
    def __init__(self):
        self.vllm_url = settings.VLLM_URL
        self.model = settings.MODEL_NAME
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> dict:
        """
        Generate completion using vLLM server.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream responses (not implemented)
        
        Returns:
            dict: OpenAI-compatible chat completion response
        
        Raises:
            Exception: If vLLM request fails
        """
        if stream:
            raise NotImplementedError("Streaming not yet supported")
        
        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            logger.info(f"Sending request to vLLM: {len(messages)} messages")
            start_time = time.time()
            
            response = await self.client.post(
                f"{self.vllm_url}/chat/completions",
                json=request_data
            )
            
            response.raise_for_status()
            result = response.json()
            
            duration = time.time() - start_time
            logger.info(
                f"vLLM response received in {duration:.2f}s, "
                f"tokens: {result.get('usage', {}).get('completion_tokens', 0)}"
            )
            
            return result
        
        except httpx.HTTPStatusError as e:
            logger.error(f"vLLM HTTP error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"vLLM request failed: {e.response.text}")
        
        except httpx.RequestError as e:
            logger.error(f"vLLM connection error: {str(e)}")
            raise Exception(f"Cannot connect to vLLM server at {self.vllm_url}")
        
        except Exception as e:
            logger.error(f"Unexpected error in inference: {str(e)}")
            raise
    
    async def health_check(self) -> bool:
        """
        Check if vLLM server is healthy.
        
        Returns:
            bool: True if server is responding
        """
        try:
            response = await self.client.get(f"{self.vllm_url}/models")
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
