# Week 1: LLM Inference Service

**Goal:** Deploy a production-grade LLM API with monitoring and observability

**Duration:** 5-8 hours total

---

## 🎯 Learning Objectives

1. **AI Engineering:**
   - Understand LLM inference optimization (continuous batching, KV caching)
   - Implement production monitoring stack
   - Handle rate limiting and authentication

2. **Software Architecture (Ch1-2):**
   - Apply **layered architecture** pattern
   - Separate concerns (API, business logic, model inference)
   - Design for modularity

3. **Practical Skills:**
   - Deploy vLLM inference server
   - Build FastAPI wrapper with authentication
   - Set up Prometheus + Grafana monitoring
   - Conduct load testing with Locust

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   API Layer                         │
│  ┌──────────────────────────────────────────────┐  │
│  │  FastAPI Service                             │  │
│  │  - Authentication (API Key)                  │  │
│  │  - Rate Limiting                             │  │
│  │  - Request Validation                        │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                Business Logic Layer                 │
│  ┌──────────────────────────────────────────────┐  │
│  │  Inference Manager                           │  │
│  │  - Request Queue                             │  │
│  │  - Response Formatting                       │  │
│  │  - Error Handling                            │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                 Model Layer                         │
│  ┌──────────────────────────────────────────────┐  │
│  │  vLLM Server                                 │  │
│  │  - Model: Qwen2.5-7B-Instruct                │  │
│  │  - GPU Acceleration                          │  │
│  │  - Continuous Batching                       │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│              Observability Layer                    │
│  ┌──────────────────────────────────────────────┐  │
│  │  Prometheus (Metrics)                        │  │
│  │  - Request latency                           │  │
│  │  - Throughput (tokens/sec)                   │  │
│  │  - GPU utilization                           │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Grafana (Visualization)                     │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
week-01-llm-inference/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── docker-compose.yml         # Multi-container setup
│
├── src/
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py         # API endpoints
│   │   └── auth.py           # API key authentication
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration management
│   │   └── inference.py      # vLLM client wrapper
│   └── monitoring/
│       ├── __init__.py
│       └── metrics.py        # Prometheus metrics
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py           # API endpoint tests
│   └── test_inference.py     # Inference logic tests
│
├── monitoring/
│   ├── prometheus.yml        # Prometheus config
│   └── grafana/
│       └── dashboards/
│           └── llm-inference.json  # Grafana dashboard
│
├── scripts/
│   ├── setup.sh              # Environment setup
│   ├── start_vllm.sh         # Start vLLM server
│   └── load_test.py          # Locust load testing
│
└── docs/
    ├── architecture.md       # Architecture Decision Record
    ├── api-spec.md           # API documentation
    └── performance.md        # Load testing results
```

---

## 🚀 Implementation Steps

### Step 1: Environment Setup (30 min)

```bash
# Create project directory
cd Andromeda/week-01-llm-inference

# Set up Python environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install vllm fastapi uvicorn prometheus-client python-dotenv locust
pip freeze > requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### Step 2: Deploy vLLM Server (45 min)

**Option A: Local GPU**
```bash
# Download model (requires HuggingFace CLI)
huggingface-cli download Qwen/Qwen2.5-7B-Instruct

# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000 \
    --gpu-memory-utilization 0.9
```

**Option B: CPU-only (for testing)**
```bash
# Use smaller model
python -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8000
```

### Step 3: Build FastAPI Wrapper (1.5 hours)

See `src/main.py` for implementation.

**Key Features:**
- API key authentication
- Rate limiting (10 requests/min per key)
- Request/response logging
- Prometheus metrics export

### Step 4: Set Up Monitoring (1 hour)

**Prometheus Configuration:**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'llm-api'
    static_configs:
      - targets: ['localhost:8080']
```

**Start Monitoring Stack:**
```bash
docker-compose up -d prometheus grafana
```

### Step 5: Load Testing (1 hour)

```bash
# Run Locust tests
locust -f scripts/load_test.py --host=http://localhost:8080
```

**Test Scenarios:**
- Sustained load: 10 users, 1 req/sec
- Burst traffic: 50 users, 10 req/sec
- Measure: p50, p95, p99 latency

### Step 6: Documentation (1 hour)

Write the following docs:
1. **Architecture Decision Record (ADR)**
   - Why layered architecture?
   - Why vLLM over alternatives?
   - Trade-offs: latency vs cost

2. **API Specification**
   - POST `/v1/chat/completions`
   - Authentication header format
   - Rate limit headers

3. **Performance Report**
   - Latency benchmarks
   - Throughput (tokens/sec)
   - GPU utilization

---

## 🧪 Testing Checklist

- [ ] API responds to valid requests
- [ ] Authentication rejects invalid API keys
- [ ] Rate limiting blocks excessive requests
- [ ] Prometheus metrics are exported
- [ ] Grafana dashboard displays metrics
- [ ] Load test completes without errors

---

## 📊 Success Metrics

By the end of Week 1, you should have:
- ✅ Working LLM API (local or deployed)
- ✅ Monitoring dashboard with live metrics
- ✅ Architecture design document
- ✅ Load testing report

**Minimum Viable Product:**
- API handles 10 req/sec
- P95 latency < 2 seconds
- Uptime > 99% during 1-hour test

---

## 🔗 Resources

**Documentation:**
- [vLLM Quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)

**Similar Projects:**
- [OpenAI-compatible API with vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)
- [Production LLM Serving Guide](https://huggingface.co/docs/text-generation-inference/index)

---

## 🎓 Learning Review

After completing this week, answer:

1. **Architecture:** Why is layered architecture suitable for this API?
2. **Trade-offs:** What did you sacrifice for performance (latency, cost, complexity)?
3. **Monitoring:** Which metric is most critical for detecting issues?
4. **Next Steps:** How would you scale this to 1000 req/sec?

Document your answers in `docs/week-01-reflection.md`.

---

## 🐛 Common Issues

**vLLM fails to start:**
- Check GPU memory: `nvidia-smi`
- Reduce `--gpu-memory-utilization` to 0.7

**API returns 500 errors:**
- Check vLLM server logs
- Verify model path is correct

**Metrics not showing in Grafana:**
- Confirm Prometheus is scraping: `http://localhost:9090/targets`
- Check FastAPI metrics endpoint: `http://localhost:8080/metrics`

---

**Next Week:** [Week 2 - Data Pipeline →](../week-02-data-pipeline/README.md)
