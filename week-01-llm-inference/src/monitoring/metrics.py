"""
Prometheus metrics for monitoring.

Metrics tracked:
- Request count (by endpoint, method, status code)
- Request duration (histogram)
- Active requests (gauge)
- Error count (by type)
- Token usage (if available)
"""

from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_counter = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status_code']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0)
)

active_requests = Gauge(
    'api_active_requests',
    'Number of active requests'
)

# Error metrics
error_counter = Counter(
    'api_errors_total',
    'Total API errors',
    ['endpoint', 'error_type']
)

# Token metrics
tokens_generated = Counter(
    'llm_tokens_generated_total',
    'Total tokens generated',
    ['model']
)

tokens_input = Counter(
    'llm_tokens_input_total',
    'Total input tokens processed',
    ['model']
)

# Inference metrics
inference_duration = Histogram(
    'llm_inference_duration_seconds',
    'LLM inference duration',
    ['model'],
    buckets=(0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0)
)

inference_tokens_per_second = Histogram(
    'llm_tokens_per_second',
    'Tokens generated per second',
    ['model'],
    buckets=(5, 10, 20, 50, 100, 200)
)
