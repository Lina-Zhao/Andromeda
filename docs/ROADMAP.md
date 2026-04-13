# Andromeda — Detailed Roadmap

---

## Phase 1: Pattern Drills (Week 1-4)

> 目标：每周 2-3h，练一种架构 pattern + 一种 AI 编排技术
> 核心：做完能向别人讲清楚 pattern 的 trade-off

---

### Week 1: Layered Architecture + Harness Engineering

**架构概念：** Layered Architecture（分层架构）
- 关注点分离：Presentation → Business Logic → Persistence
- Trade-off：清晰的边界 vs 性能损耗（层间调用开销）
- 书中对应：Fundamentals of Software Architecture Ch-10

**AI 概念：** Prompt → Context → Harness 三代演进
- Prompt Engineering：问什么
- Context Engineering：给模型什么上下文让它回答好
- Harness Engineering：模型运行的整个环境（工具、权限、状态、guardrails、eval、重试）
- 参考：Anthropic long-running agents, Mitchell Hashimoto's harness framing

**练习：重构一个 Chatbot**
1. V1 — 单 prompt 的 chatbot（直接调 API，无结构）
2. V2 — 分层架构：API Layer / Business Logic / LLM Layer，加 context management
3. V3 — 加 harness：input validation, output guardrails, structured logging, retry logic, eval checks
4. 写 ADR：为什么分层？每一层的职责？harness 加了什么可靠性保证？

**产出清单：**
- [ ] V1/V2/V3 三个版本的代码
- [ ] ADR: `docs/adr-001-layered-chatbot.md`
- [ ] 一段话总结：Layered Architecture 适合什么场景，不适合什么场景

---

### Week 2: Microkernel Architecture + Tool Calling

**架构概念：** Microkernel / Plugin Architecture
- 核心系统 + 可插拔插件
- Trade-off：扩展性极强 vs 插件间通信复杂、核心系统设计要求高
- 书中对应：Fundamentals of Software Architecture Ch-12

**AI 概念：** Function Calling / Tool Use
- LLM 如何决定调用哪个工具
- Tool schema 设计：清晰的函数签名 = 更准确的调用
- 错误处理：工具调用失败时的 fallback 策略
- 参考：AI Engineering Ch-5 (Tool Use), Building AI Agents Ch-4

**练习：可插拔工具的 CLI Agent**
1. 设计核心系统：agent loop（接收输入 → 推理 → 选择工具 → 执行 → 返回结果）
2. 实现插件接口：每个工具是一个独立模块，遵循统一接口
3. 实现 3-5 个插件：文件操作、Web 搜索、计算器、天气查询等
4. 动态加载：运行时注册/卸载插件
5. 写 ADR：为什么用 Microkernel？插件接口怎么设计的？

**产出清单：**
- [ ] CLI agent + 至少 3 个插件
- [ ] 插件接口文档
- [ ] ADR: `docs/adr-002-microkernel-agent.md`
- [ ] 一段话总结：Microkernel 的核心设计决策

---

### Week 3: Pipeline Architecture + Sequential Agent Orchestration

**架构概念：** Pipeline Architecture
- Filter-and-pipe：数据流过一系列处理 stage
- Trade-off：每个 stage 独立、可替换 vs 不适合需要共享状态的场景
- 书中对应：Fundamentals of Software Architecture Ch-11

**AI 概念：** Sequential Agent Orchestration
- Agent chain：一个 agent 的输出是下一个的输入
- 每个 agent 专注一个任务（专业化 > 全能）
- 中间状态传递：structured output 作为 contract
- 参考：Azure Architecture Center — Sequential Orchestration Pattern

**练习：文档处理 Pipeline**
1. 设计 pipeline：Raw Text → Summarizer Agent → Translator Agent → Formatter Agent → Output
2. 每个 stage 是一个独立 agent，有明确的输入/输出 schema
3. 加 error handling：某个 stage 失败时的降级策略
4. 加 observability：每个 stage 的耗时、token 用量、输出质量评分
5. 写 ADR：为什么用 Pipeline？stage 之间的 contract 怎么设计？

**产出清单：**
- [ ] 文档处理 pipeline（至少 3 个 stage）
- [ ] 每个 stage 的输入/输出 schema 文档
- [ ] ADR: `docs/adr-003-pipeline-agents.md`
- [ ] 一段话总结：Pipeline pattern 和 sequential orchestration 的 match/mismatch

---

### Week 4: Event-Driven Architecture + Async Agent Communication

**架构概念：** Event-Driven Architecture
- Broker topology vs Mediator topology
- Trade-off：松耦合 + 高扩展性 vs 调试困难、事件顺序不保证
- 书中对应：Fundamentals of Software Architecture Ch-14

**AI 概念：** Agent 间异步通信
- 发布/订阅模式：agent 发布事件，其他 agent 订阅并响应
- Handoff pattern：一个 agent 将任务移交给另一个
- 并发 agents：多个 agent 同时处理不同子任务
- 参考：Azure Architecture Center — Concurrent + Handoff Patterns

**练习：事件驱动的多 Agent 通知系统**
1. 设计事件系统：Monitor Agent 检测变化 → 发布事件 → Analyzer Agent 分析 → Notifier Agent 通知
2. 使用消息队列或简单的 pub/sub（Redis, 或自建 in-memory event bus）
3. Agent 之间不直接调用，只通过事件通信
4. 加 dead letter queue：处理失败的事件
5. 写 ADR：为什么用 Event-Driven？和 Pipeline 相比有什么不同？

**产出清单：**
- [ ] 事件驱动的 multi-agent 系统
- [ ] 事件 schema + 系统架构图
- [ ] ADR: `docs/adr-004-event-driven-agents.md`
- [ ] 一段话总结：Event-Driven 的力量和代价

---

## Phase 2: Deep Projects (Week 5-10)

> 目标：组合多个 pattern + multi-agent 编排，从设计到交付
> 核心：先画架构再写代码，harness 可靠性，复盘迭代

---

### Project 1: AI Code Review System (Week 5-7)

**概述：** 构建一个自动化代码审查系统，多个 agent 协作完成不同维度的审查。

**涉及 Pattern：**
- Microkernel（审查规则作为插件）
- Pipeline（代码经过多轮审查）
- Event-Driven（审查结果触发通知/action）

**Multi-Agent 编排：**
- Style Agent — 代码风格、命名规范
- Security Agent — 安全漏洞扫描
- Architecture Agent — 是否符合架构规范
- Reporter Agent — 汇总所有审查结果，生成报告
- Orchestrator — 协调 agent 执行顺序、处理冲突

**Harness 要求：**
- 输入验证：只接受合法的代码文件
- Agent output eval：每个 agent 的结果要通过可信度评分
- Retry + fallback：某个 agent 超时或返回低质量结果时的处理
- Structured logging：完整的审查过程可追溯

**Week 5:** 架构设计 + 核心 agent 实现
**Week 6:** 完整 pipeline + harness + eval
**Week 7:** 集成测试 + demo + 复盘文档

**产出清单：**
- [ ] 架构设计文档（Week 5 开始前完成）
- [ ] Multi-agent 编排方案
- [ ] Harness 设计文档
- [ ] 可 demo 的系统
- [ ] 复盘：`docs/project-1-retrospective.md`

---

### Project 2: Knowledge Assistant (Week 8-10)

**概述：** 构建一个能回答领域知识问题的 AI 助手，支持文档检索 + 多轮对话 + agent 协作。

**涉及 Pattern：**
- Layered Architecture（API / Service / Data layer）
- Microservices（Embedding Service + Retrieval Service + Generation Service 分离）
- CQRS（读路径和写路径分离）

**Multi-Agent 编排：**
- Router Agent — 判断用户意图，分发到正确的处理流
- Retrieval Agent — 搜索知识库，返回相关文档
- Synthesis Agent — 基于检索结果生成回答
- Fact-Check Agent — 验证回答是否有文档依据
- Handoff pattern：复杂问题从 Router → Retrieval → Synthesis → Fact-Check

**Harness 要求：**
- Citation 验证：回答必须有来源
- Hallucination detection：和检索文档对比，标记无依据的内容
- 上下文管理：多轮对话的 context window 管理策略
- Eval pipeline：自动化评估回答质量（faithfulness, relevance, completeness）

**Week 8:** 架构设计 + RAG 核心
**Week 9:** Multi-agent 编排 + harness
**Week 10:** Eval pipeline + demo + 复盘

**产出清单：**
- [ ] 架构设计文档
- [ ] RAG pipeline + Multi-agent 编排
- [ ] Eval 结果报告
- [ ] 可 demo 的系统
- [ ] 复盘：`docs/project-2-retrospective.md`

---

## Phase 3: Capstone (Week 11-12)

> 目标：独立完成一个完整系统，Argo 只 review 不代写
> 选题在 Phase 2 结束后根据能力和兴趣确定

**候选方向（仅参考，不限于此）：**
1. 工作相关：基于实际工作场景的工具/系统
2. 个人项目：解决自己的真实问题
3. 开源贡献：给现有项目添加 AI 能力

**硬性要求：**
- [ ] 独立完成架构设计文档（提交给 Argo review）
- [ ] 使用 multi-agent 协作开发
- [ ] 完整 harness：guardrails, eval, monitoring
- [ ] 能向非技术人员解释系统做了什么
- [ ] 能向技术人员解释每个架构决策的 why
- [ ] Technical presentation（PPT 或 doc）

---

## Templates

### ADR Template

```markdown
# ADR-XXX: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed / Accepted / Deprecated

## Context
What is the problem? What forces are at play?

## Decision
What did you decide and why?

## Alternatives Considered
What else did you consider? Why did you reject them?

## Consequences
- Positive:
- Negative:
- Trade-offs:

## References
- Book chapters, articles, patterns
```

---

_Last updated: 2026-04-13_
