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

## Alternatives Considered

None. This is intentionally the simplest architecture pattern — the goal is to start from the basics and build up. Layered Architecture is the first pattern in the architecture book and the most straightforward to implement.

## Consequences

- **Positive:** Simple, easy to understand, fast to implement. Good for learning and getting something working quickly.
- **Negative:** Not easy to scale or extend in the future. Adding new features may require changes across multiple layers.
- **Trade-offs:** Sacrificing extensibility and elasticity for simplicity — and that's an acceptable trade-off right now. Scalability is the least important quality attribute at this stage.
