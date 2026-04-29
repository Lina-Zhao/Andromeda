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
┌─────────────────────────┐
│   Presentation Layer    │  CLI / UI
├─────────────────────────┤
│   Orchestration Layer   │  Guardrails, Retry, Token Budget, Safety
│   ┌───────┐ ┌────────┐  │
│   │  LLM  │ │  Data  │  │
│   └───────┘ └────────┘  │
└─────────────────────────┘
```

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

**User Profile:**
- `id` — unique identifier
- `name` — user name
- `height` — cm
- `weight` — kg (support 斤 input, convert internally: 1kg = 2斤)
- `target_weight` — kg (support 斤 input, convert internally)
- (extensible for future fields: age, conditions, equipment, etc.)

## Alternatives Considered

Considered **Microkernel (Plugin) Architecture** — but the current scope doesn't warrant it. There are no pluggable modules or dynamic extensions needed yet. Layered is the simplest pattern and the right starting point for this exercise.

## Consequences

- **Positive:** Simple, easy to understand, fast to implement. Good for learning and getting something working quickly.
- **Negative:** Not easy to scale or extend in the future. Adding new features may require changes across multiple layers.
- **Trade-offs:** Sacrificing extensibility and elasticity for simplicity — and that's an acceptable trade-off right now. Scalability is the least important quality attribute at this stage.
