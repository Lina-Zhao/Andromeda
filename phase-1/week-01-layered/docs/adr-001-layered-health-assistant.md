# ADR-001: Layered Architecture for Health Assistant Chatbot

**Date:** 2026-04-29
**Status:** Accepted

## Context

Health is the foundation of everything — but at 30, it's hard to know how to approach it systematically. There's too much noise online (extreme running routines that wear the body down, making people look 60 at 40), and no personalized guidance. I need a health expert that understands my situation and helps me build a sustainable, healthy lifestyle — not one-size-fits-all internet advice.

This is also the first exercise in Andromeda Phase 1. The goal is to practice Layered Architecture with a real use case, starting from the simplest possible structure.

## Decision

Build a health assistant chatbot using a Layered Architecture with the following layers:

1. **Presentation Layer** — Pure UI, handles user input/output only
2. **Service Layer** — Receives requests from the Presentation layer, orchestrates the processing logic:
   - Orchestrator: request handling, guardrails, tool integration, safety checks
   - LLM integration: assembles context and sends to the LLM
3. **Data Layer** — Persists user data (health profile, conversation history, preferences)

Each layer only depends on the layer directly below it. No cross-layer shortcuts.

```
┌──────────────────┐
│   Presentation   │   CLI / UI
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Orchestration  │   Guardrails · Retry · Token Budget · Safety
└──┬────────────┬──┘
   │            │
   ▼            ▼
┌──────┐    ┌──────┐
│ LLM  │    │ Data │
└──────┘    └──────┘
```

**Dependency rules:**
- Each layer only depends downward; no upward or skip-layer calls.
- LLM and Data are siblings — they do **not** depend on each other. The LLM layer is intentionally stateless and has no knowledge of who the user is. All user context is injected by Orchestration into the prompt before calling LLM.
- This boundary is what makes the LLM layer a swappable adapter (change provider in 1 place) and the Data layer independently testable.

### Quality Criteria — What Makes a Good Health Chatbot

A good health assistant must be **comprehensive, safe, personalized, and evidence-based**:

- **Comprehensive:** e.g. weight loss advice must cover diet, hydration, sleep — not just "eat less, exercise more"
- **Personalized:** Must ask about the user's conditions first (gym access? equipment? schedule?) before giving plans
- **Safe:** Must validate user goals against objective reality (e.g. 160cm targeting 30kg → refuse and explain why)
- **Evidence-based:** Diet is fundamental — weight loss = caloric deficit (input < output). Must address nutrition, not just exercise

### Guardrails

**Input:**
- Topic validation — only respond to health-related topics
- User info completeness — proactively ask for missing info before giving advice
- User data anonymization / desensitization

**Output:**
- Unified response format
- Hallucination detection — do not fabricate medical claims

**Orchestration:**
- Retry logic for LLM failures
- Token budget management
- Safety checks on user goals before executing plans

### Data Schema

**User Profile (static / slow-changing):**
- `id` — unique identifier
- `name` — user name
- `height_cm`
- `weight_kg` — current (support 斤 input, convert internally: 1kg = 2斤)
- `target_weight_kg` — goal (support 斤 input, convert internally)
- `injuries` — list of strings (e.g. `["left knee", "lower back"]`)
- `equipment` — list of strings (e.g. `["gym", "dumbbells", "treadmill"]`)
- `dietary_constraints` — list of strings (e.g. `["low-carb", "vegetarian"]`)

**Daily Log (rolling, last 7 days minimum):**
- `date`
- `weight_kg`
- `exercise` — `{ type, duration_min, intensity }`
- `sleep` — `{ hours, quality_1to10 }`
- `water_ml`
- `diet_notes` — free text

**Storage choice (Phase 1):** single JSON file under `data/` — simplest possible, easy to inspect. Will migrate to SQLite if/when query patterns need it.

## Alternatives Considered

**1. Single-file, direct LLM call (the default "just ship it" approach).**
Technically able to add guardrails inline, but quickly degrades into an unmaintainable mess:
- *Concerns tangled:* UI prompts, guardrail checks, retry logic, token counting, and data access all live in one file — every change requires reading the whole file.
- *Untestable:* Can't unit-test a single guardrail without mocking the entire LLM call chain.
- *Not swappable:* Switching LLM provider (OpenAI → Claude) means hunting through the file because prompt assembly and provider call are fused.
- *Not reusable:* Phase 2 (microkernel) and Phase 3 (pipeline) need the same guardrails and LLM adapter — a single-file version can't be lifted out, every phase rewrites from scratch.
Layered pays a small structural cost up front to buy all of these capabilities. Worth it as the Phase 1 starting point.

**2. Microkernel (Plugin) Architecture.**
Attractive long-term (each guardrail / tool as a plugin), but the current scope has no pluggable modules or dynamic extensions yet. Adopting it now would be premature abstraction. Layered first, microkernel in Phase 2 when the need is real.

## Consequences

- **Positive:** Simple, easy to understand, fast to implement. Good for learning and getting something working quickly.
- **Negative:** Not easy to scale or extend in the future. Adding new features may require changes across multiple layers.
- **Trade-offs:** Sacrificing extensibility and elasticity for simplicity — and that's an acceptable trade-off right now. Scalability is the least important quality attribute at this stage.
