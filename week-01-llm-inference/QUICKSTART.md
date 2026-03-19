# 🚀 Quick Start Guide

This guide will help you get Week 1's LLM Inference Service running in 10 minutes.

---

## Prerequisites

- Python 3.10+
- Docker & Docker Compose (for monitoring)
- (Optional) CUDA-capable GPU for local LLM inference

---

## Setup Steps

### 1. Environment Setup

```bash
cd week-01-llm-inference
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Configure Environment

Edit `.env` with your settings:

```bash
# Minimum required changes:
API_KEYS=your-secret-key-here
```

### 3. Start vLLM Server (Choose one option)

**Option A: Use OpenAI API (Recommended for testing)**

Edit `.env`:
```bash
VLLM_URL=https://api.openai.com/v1
# Add your OpenAI key to API_KEYS
```

**Option B: Local vLLM with GPU**

```bash
# In a separate terminal
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000
```

**Option C: Use smaller model (CPU-only)**

```bash
python -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8000
```

### 4. Start API Server

```bash
source venv/bin/activate
python -m src.main
```

API will be available at: `http://localhost:8080`

### 5. Test the API

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer your-secret-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello! What is 2+2?"}
    ],
    "max_tokens": 100
  }'
```

### 6. Start Monitoring (Optional)

```bash
docker-compose up -d
```

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)

---

## API Endpoints

### Chat Completion
```
POST /v1/chat/completions
Authorization: Bearer YOUR_API_KEY
```

### List Models
```
GET /v1/models
Authorization: Bearer YOUR_API_KEY
```

### Health Check
```
GET /health
```

### Metrics
```
GET /metrics
```

---

## Interactive API Docs

Visit `http://localhost:8080/docs` for Swagger UI with:
- Live API testing
- Request/response schemas
- Authentication examples

---

## Load Testing

```bash
# Start Locust
locust -f scripts/load_test.py --host=http://localhost:8080

# Open browser to http://localhost:8089
# Set users: 10, spawn rate: 1
```

---

## Troubleshooting

### API returns 401 Unauthorized
- Check `Authorization` header format: `Bearer YOUR_KEY`
- Verify key exists in `.env` `API_KEYS`

### API returns 500 Internal Server Error
- Check vLLM server is running: `curl http://localhost:8000/v1/models`
- Check API logs for detailed error

### Rate limit exceeded (429)
- Default limit: 10 requests/minute
- Increase in `.env`: `RATE_LIMIT_PER_MINUTE=100`

### Prometheus shows no data
- Check API is exposing metrics: `curl http://localhost:8080/metrics`
- Verify Prometheus targets: `http://localhost:9090/targets`

---

## Next Steps

1. Read [Architecture Design Doc](docs/architecture.md)
2. Run load tests and document results
3. Implement streaming support
4. Add Redis for rate limiting
5. Deploy to cloud (Railway, Render, etc.)

---

**Having issues?** Check the [main README](README.md) for detailed documentation.
