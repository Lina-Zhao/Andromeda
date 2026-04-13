# 🌠 Andromeda

> _"From reading to building — architecture × AI agents × real systems."_

**Andromeda** is a progressive practice project that bridges the gap between "I've read it" and "I can build it."

Three knowledge pillars → one integrated skill set:
- 🏗️ **Software Architecture** — patterns, trade-offs, ADRs
- 🤖 **AI Agent Engineering** — orchestration, harness design, multi-agent systems
- ⚡ **AI-Augmented Development** — using AI as a force multiplier, not just a code generator

Part of the **[Celestia Lab](https://github.com/Lina-Zhao)** series.

---

## 🎯 Mission

**Problem:** Reading architecture books and AI engineering books doesn't mean you can design systems or orchestrate agents.

**Solution:** A three-phase progressive training program:
1. **Build muscle memory** — small focused exercises (2-3h each)
2. **Go deep** — multi-week projects combining patterns
3. **Prove it** — one real system from zero to production

**Not a portfolio factory.** This is a training ground for becoming an architect who can leverage AI agents to multiply output.

---

## 📅 Three-Phase Roadmap

### Phase 1: Pattern Drills (Week 1-4)
> 每周 1 个 2-3h 小练习，练一种架构 pattern + 一种 AI 编排技术

| Week | Architecture Pattern | AI Skill | Exercise |
|------|---------------------|----------|----------|
| **1** | Layered Architecture | Prompt → Context → Harness 演进 | 重构一个 chatbot：从单 prompt 到带 guardrails 的 harness |
| **2** | Microkernel (Plugin) | Tool Calling + Function Routing | 构建一个可插拔工具的 CLI agent |
| **3** | Pipeline Architecture | Sequential Agent Orchestration | 数据处理 pipeline：每个 stage 是一个 agent |
| **4** | Event-Driven Architecture | Agent 间异步通信 | 事件驱动的 multi-agent 通知系统 |

每个练习必须产出：
- ✅ 可运行的代码
- ✅ ADR（Architecture Decision Record）— 为什么选这个 pattern，trade-off 是什么
- ✅ 一段话总结：如果给别人解释这个 pattern，你怎么说？

### Phase 2: Deep Projects (Week 5-10)
> 2 个深度项目，每个 3 周，组合多个 pattern + multi-agent 编排

| Project | Duration | Patterns | AI Focus |
|---------|----------|----------|----------|
| **P1: AI Code Review System** | Week 5-7 | Microkernel + Pipeline + Event-Driven | Multi-agent: Analyzer → Reviewer → Reporter，harness design，自动化 eval |
| **P2: Knowledge Assistant** | Week 8-10 | Microservices + CQRS + Layered | RAG + Agent Orchestration（sequential + handoff），harness 迭代 |

每个项目必须产出：
- ✅ 架构设计文档（before coding）
- ✅ Multi-agent 编排方案 + 为什么这样编排
- ✅ Harness 设计：guardrails, checkpoints, eval criteria
- ✅ 可 demo 的系统
- ✅ 复盘：哪里设计对了，哪里要改

### Phase 3: Capstone (Week 11-12)
> 1 个完整系统：真实问题，从零到一

选题在 Phase 2 结束后根据能力和兴趣确定。要求：
- 独立完成架构设计（Argo 只 review，不代写）
- 使用 multi-agent 协作开发
- 完整闭环：需求 → 设计 → 实现 → 测试 → 部署 → 文档
- 能向别人讲清楚每个架构决策的 why

---

## 📚 Knowledge Sources

**已读（核心参考）：**
- [AI Engineering](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) — Chip Huyen
- [Building Applications with AI Agents](https://www.oreilly.com/) — Michael Albada
- [Fundamentals of Software Architecture, 2nd Ed](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/) — Neal Ford (reading, Ch-15 done)

**补充学习（按需）：**
- [AI Agent Orchestration Patterns — Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- Harness Engineering（Anthropic's long-running agents, Mitchell Hashimoto's framing）
- [LangGraph](https://langchain-ai.github.io/langgraph/) / [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/) / [AutoGen](https://microsoft.github.io/autogen/)

---

## 📊 Project Structure

```
andromeda/
├── README.md
├── docs/
│   └── ROADMAP.md              # Detailed weekly plans
├── phase-1/
│   ├── week-01-layered/        # Layered + Harness Engineering
│   ├── week-02-microkernel/    # Microkernel + Tool Calling
│   ├── week-03-pipeline/       # Pipeline + Sequential Agents
│   └── week-04-event-driven/   # Event-Driven + Async Agents
├── phase-2/
│   ├── project-1-code-review/  # AI Code Review System
│   └── project-2-knowledge/    # Knowledge Assistant
├── phase-3/
│   └── capstone/               # Final Project
└── templates/
    └── adr-template.md         # Architecture Decision Record template
```

---

## 🧭 Design Principles

1. **Language-agnostic** — 用最适合场景的语言，不限 Python/JS/C#
2. **Architecture-first** — 先画设计，再写代码。每个项目都从 ADR 开始
3. **AI as collaborator** — 不是让 AI 帮你写代码，是你设计系统然后编排 AI 来协作完成
4. **Harness > Prompt** — 关注系统可靠性，不只是模型输出质量
5. **做完能讲** — 如果你不能向别人解释为什么这样设计，就不算学会

---

## 📈 Progress

| Phase | Item | Status |
|-------|------|--------|
| 1 | Week 01 - Layered + Harness | ⏳ Next |
| 1 | Week 02 - Microkernel + Tool Calling | ⏳ Planned |
| 1 | Week 03 - Pipeline + Sequential Agents | ⏳ Planned |
| 1 | Week 04 - Event-Driven + Async Agents | ⏳ Planned |
| 2 | Project 1 - AI Code Review System | ⏳ Planned |
| 2 | Project 2 - Knowledge Assistant | ⏳ Planned |
| 3 | Capstone | ⏳ Planned |

---

_Redesigned: 2026-04-13 · Original: 2026-03-19_
