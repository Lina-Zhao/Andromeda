# 🌠 Andromeda

> _"Bridging theory and practice in AI Engineering — one week, one system."_

**Andromeda** is a 12-week intensive practice project that transforms theoretical knowledge from AI Engineering, AI Agents, and Software Architecture into production-grade applications.

Part of the **[Celestia Lab](https://github.com/Lina-Zhao)** series.

---

## 🎯 Mission

**Problem:** Reading books on AI Engineering and Software Architecture doesn't translate to real-world skills.

**Solution:** Build one complete AI system every week, integrating:
- 📚 **AI Engineering** (Chip Huyen) — MLOps, deployment, monitoring
- 🤖 **AI Agents** (Michael Albada) — ReAct, tool calling, multi-agent systems
- 🏗️ **Software Architecture** (Neal Ford) — Design patterns, trade-offs, scalability

**Output:** A portfolio of 12+ deployable projects + architecture docs for interviews.

---

## 📅 12-Week Roadmap

### 🔧 Phase 1: AI Engineering Foundations (Week 1-4)

| Week | Project | Tech Stack | Architecture Focus |
|------|---------|-----------|-------------------|
| **1** | LLM Inference Service | vLLM, FastAPI, Prometheus | Layered Architecture |
| **2** | Data Pipeline | Airflow, DuckDB, Qdrant | Modularity & ETL |
| **3** | Model Fine-tuning | LoRA, MLflow, PyTorch | Experiment Tracking |
| **4** | A/B Testing Framework | Redis, FastAPI | Traffic Routing |

### 🤖 Phase 2: AI Agents Applications (Week 5-8)

| Week | Project | Tech Stack | Architecture Focus |
|------|---------|-----------|-------------------|
| **5** | ReAct Agent | LangChain, Function Calling | Microkernel (Plugin System) |
| **6** | RAG System | LlamaIndex, Reranker | Retrieval Pipeline |
| **7** | Multi-Agent System | AutoGen, Redis | Inter-Service Communication |
| **8** | Agent Observability | LangSmith, OpenTelemetry | Distributed Tracing |

### 🏗️ Phase 3: Production Systems (Week 9-12)

| Week | Project | Tech Stack | Architecture Focus |
|------|---------|-----------|-------------------|
| **9** | Microservices Refactor | gRPC, Nginx, Docker | Service Boundaries |
| **10** | Event-Driven System | Kafka, Celery, WebSocket | Async Processing |
| **11** | Security & Cost Optimization | JWT, LiteLLM, Caching | Trade-offs Analysis |
| **12** | Final Project | Full Stack | Complete System Design |

---

## 🛠️ Tech Stack

**Core Technologies:**
- **LLM:** vLLM, Hugging Face Transformers, OpenAI API
- **Frameworks:** LangChain, LlamaIndex, AutoGen
- **Infrastructure:** Docker, Kubernetes, Airflow
- **Monitoring:** Prometheus, Grafana, LangSmith
- **Databases:** PostgreSQL, Redis, Qdrant (Vector DB)
- **Message Queue:** Kafka, RabbitMQ, Celery

**Languages:** Python (primary), Bash (scripting)

---

## 📊 Project Structure

```
Andromeda/
├── README.md                    # This file
├── docs/
│   ├── architecture/            # ADRs & system design docs
│   ├── learning-notes/          # Weekly reading summaries
│   └── deployment-guides/       # Production deployment steps
├── week-01-llm-inference/       # Week 1: LLM API Service
│   ├── src/                     # Source code
│   ├── tests/                   # Unit & integration tests
│   ├── docker/                  # Containerization
│   ├── docs/                    # Week-specific docs
│   └── README.md                # Project-specific guide
├── week-02-data-pipeline/       # Week 2: Data Pipeline
├── ...
├── week-12-final-project/       # Week 12: Capstone
├── scripts/                     # Utility scripts
│   ├── setup.sh                 # Environment setup
│   └── deploy.sh                # Deployment automation
└── .github/
    └── workflows/               # CI/CD pipelines
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- CUDA-capable GPU (optional, for local LLM inference)
- 16GB+ RAM recommended

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Lina-Zhao/Andromeda.git
cd Andromeda

# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Navigate to Week 1 project
cd week-01-llm-inference
./setup.sh
```

---

## 📚 Learning Resources

**Books (Core References):**
- [AI Engineering](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) - Chip Huyen
- [Building Applications with AI Agents](https://www.oreilly.com/) - Michael Albada
- [Fundamentals of Software Architecture](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/) - Neal Ford

**Complementary Materials:**
- [LangChain Documentation](https://python.langchain.com/)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Martin Fowler's Architecture Blog](https://martinfowler.com/architecture/)

---

## 🎯 Success Metrics

**By Week 12, you should have:**
- ✅ 12 complete, deployable AI projects
- ✅ 10+ architecture design documents (ADRs)
- ✅ 3-4 production-ready systems (with monitoring & CI/CD)
- ✅ A portfolio for technical interviews

**Ultimate Goal:** Use these projects to pass AI Engineering interviews at top tech companies.

---

## 📈 Progress Tracking

| Week | Project | Status | Demo Link | Blog Post |
|------|---------|--------|-----------|-----------|
| 1 | LLM Inference Service | 🚧 In Progress | - | - |
| 2 | Data Pipeline | ⏳ Planned | - | - |
| 3 | Model Fine-tuning | ⏳ Planned | - | - |
| ... | ... | ... | ... | ... |

---

## 🤝 Contributing

This is a personal learning project, but feedback and suggestions are welcome!

- Open an issue for questions or suggestions
- Share your own implementations or improvements
- Check out other projects in the [Celestia Lab](https://github.com/Lina-Zhao)

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🌌 Celestia Lab Series

- **[Kepler](https://github.com/Lina-Zhao/Kepler)** - Personal workspace & journal system
- **[Orion](https://github.com/Lina-Zhao/Orion)** - Previous project
- **[Andromeda](https://github.com/Lina-Zhao/Andromeda)** - AI Engineering practice (this repo)

---

<div align="center">

**Built with 🧠 and ☕ in 2026**

_"The journey from theory to production, one commit at a time."_

</div>
