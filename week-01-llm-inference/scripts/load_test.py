"""
Load testing script using Locust.

Usage:
  locust -f scripts/load_test.py --host=http://localhost:8080

Then open http://localhost:8089 in browser to start test.
"""

from locust import HttpUser, task, between
import json


class LLMAPIUser(HttpUser):
    """Simulate users making requests to LLM API."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Set up authentication header."""
        self.headers = {
            "Authorization": "Bearer test-key-123",
            "Content-Type": "application/json"
        }
    
    @task(3)  # Weight: 3x more likely than other tasks
    def chat_completion_short(self):
        """Test short chat completion."""
        payload = {
            "messages": [
                {"role": "user", "content": "What is 2+2?"}
            ],
            "max_tokens": 50,
            "temperature": 0.7
        }
        
        with self.client.post(
            "/v1/chat/completions",
            headers=self.headers,
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:
                response.failure("Rate limited")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)
    def chat_completion_long(self):
        """Test longer chat completion."""
        payload = {
            "messages": [
                {"role": "user", "content": "Explain quantum computing in detail."}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        with self.client.post(
            "/v1/chat/completions",
            headers=self.headers,
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)
    def list_models(self):
        """Test models endpoint."""
        self.client.get(
            "/v1/models",
            headers=self.headers
        )
    
    @task(2)
    def health_check(self):
        """Test health endpoint."""
        self.client.get("/health")


# Test scenarios
class QuickTest(HttpUser):
    """Quick smoke test - 1 user, simple requests."""
    wait_time = between(1, 2)
    tasks = [LLMAPIUser.chat_completion_short]

class StressTest(HttpUser):
    """Stress test - multiple users, mixed requests."""
    wait_time = between(0.5, 1.5)
    tasks = [
        LLMAPIUser.chat_completion_short,
        LLMAPIUser.chat_completion_long,
        LLMAPIUser.list_models
    ]
