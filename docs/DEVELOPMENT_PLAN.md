# 开发计划 · CrossBorder-Support-Agent

> 分阶段推进，每阶段以「可运行 + 可验证」为验收标准。

---

## 0. 总体路线

```mermaid
graph LR
    P0[P0 基础设施] --> P1[P1 订单查询 MVP]
    P1 --> P2[P2 统一模型与平台适配器]
    P2 --> P3[P3 LangGraph 多 Agent 编排]
    P3 --> P4[P4 Agentic RAG]
    P4 --> P5[P5 合规护栏与 HITL]
    P5 --> P6[P6 评估与可观测]
    P6 --> P7[P7 前端与部署]
```

| 阶段 | 主题 | 状态 |
| :--- | :--- | :--- |
| P0 | 基础设施与工程骨架 | ✅ 已完成 |
| P1 | 订单查询 MVP | ✅ 已完成（基础版） |
| P2 | 统一模型与平台适配器 | ⬜ 未开始 |
| P3 | LangGraph 多 Agent 编排 | ⬜ 未开始 |
| P4 | Agentic RAG | ⬜ 未开始 |
| P5 | 合规护栏与 Human-in-the-loop | ⬜ 未开始 |
| P6 | 评估与可观测 | ⬜ 未开始 |
| P7 | 前端与部署 | ⬜ 未开始 |

---

## P0 · 基础设施与工程骨架 ✅

- [x] `pyproject.toml` 依赖声明（FastAPI / SQLAlchemy / LangGraph / Chroma 等）
- [x] `pydantic-settings` 统一配置，支持 `.env`
- [x] 异步数据库引擎与会话工厂 `get_db`
- [x] Docker Compose：PostgreSQL 16 + Chroma 1.5.9，数据卷持久化
- [x] FastAPI 入口与 `/api/health`
- [ ] 补齐 `.env.example`
- [ ] Docker Compose 增加 Redis 服务
- [ ] 引入 Alembic 迁移目录，替代 `create_all`
- [ ] 统一日志（structlog 或 logging JSON 格式）
- [ ] 配置 `pytest-asyncio` 的 `asyncio_mode = auto`

**验收标准**：`docker compose up -d` + `uvicorn` 启动后 `/api/health` 返回 200。

---

## P1 · 订单查询 MVP ✅

- [x] `Order` 模型（order_id / platform / status / paid_amount 等）
- [x] `GET /api/orders/{order_id}` 只读接口
- [x] `init_db.py` 建表 + 种子数据
- [ ] 增加分页列表接口 `GET /api/orders`
- [ ] 统一错误响应结构（`code` / `message` / `trace_id`）
- [ ] 补充接口单测（httpx AsyncClient + 测试库）
- [ ] 修复 `init_db.py` 中 "MySQL" 错误文案

**验收标准**：查询 `ORD-1001` 返回 `{"order_id","status","amount"}`；不存在返回 404。

---

## P2 · 统一模型与平台适配器 ⬜

目标：屏蔽 Amazon / Shopify / Shopee 的异构数据结构与权限差异。

- [ ] `app/schemas/unified.py`：`UnifiedOrder` / `UnifiedMessage` / `ShipmentEvent`（Pydantic v2）
- [ ] `app/adapters/base.py`：`BasePlatformAdapter` 抽象基类（`fetch_order` / `send_message` / `list_capabilities`）
- [ ] `app/adapters/factory.py`：按平台标识返回适配器实例
- [ ] `app/adapters/shopify.py`：真实沙盒 API（改地址 / 取消订单）
- [ ] `app/adapters/amazon_mock.py`：FBA/FBM 分支 + 限流模拟，无写操作
- [ ] `app/adapters/shopee_mock.py`：COD 标记 + 多语种混合消息
- [ ] `orders` 表扩展：`sku`、`tracking_no`、`fulfillment_type`、`tax_mode`
- [ ] 适配器契约单测（同一 UnifiedOrder 结构断言）

**验收标准**：三种 mock 订单经 Factory 转换后字段结构完全一致。

---

## P3 · LangGraph 多 Agent 编排 ⬜

- [ ] `app/agents/state.py`：`AgentState` TypedDict + Pydantic 校验
- [ ] `app/agents/graph.py`：`StateGraph` 拓扑 + 条件边
- [ ] `Router Node`：语种识别 + 意图分类 + 风险打分（轻量模型）
- [ ] `Order Action Node`：校验 `is_verified` → 动态绑定工具
- [ ] `Response Synthesizer`：多语言草稿生成
- [ ] `app/agents/tools.py`：按平台注册 `StructuredTool`，写操作注入 `idempotency_key`
- [ ] PostgreSQL Checkpointer（`AsyncPostgresSaver`）
- [ ] SSE / WebSocket 流式输出（可选）

**验收标准**：输入 Shopify 改地址请求 → 图正确路由到 Order 节点并返回确认；Amazon 请求无法调用改单工具。

---

## P4 · Agentic RAG ⬜

- [ ] `app/rag/ingestion.py`：PyMuPDF 解析 PDF → 父子分块 → 向量化入库
- [ ] `app/rag/retriever.py`：向量 + BM25 混合检索 + 重排
- [ ] SKU 元数据强隔离（检索强制 filter）
- [ ] 相关度阈值（0.45）+ Query Rewrite 二次检索
- [ ] 检索失败诚实兜底（禁止编造排查步骤）
- [ ] 离线检索评估脚本（Recall@K / MRR）

**验收标准**：德语 E04 报错查询命中 `SKU-CM200` 对应故障树章节，且不串其他型号。

---

## P5 · 合规护栏与 HITL ⬜

- [ ] `app/guardrails/rules.py`：URL / 邮箱 / WhatsApp / PayPal / 诱导好评正则规则
- [ ] `app/guardrails/policy.py`：Policy LLM 审查节点
- [ ] Self-Correction 回边（写入 `critique`，`max_retries=2`）
- [ ] `interrupt_before=["human_approval"]` 挂起逻辑
- [ ] 审批工单表 + 告警推送（Webhook / 飞书）
- [ ] `POST /api/approvals/{thread_id}/resume` 恢复接口
- [ ] 护栏回归用例集（违规话术样本）

**验收标准**：含 PayPal 字样的 Amazon 草稿被拦截并重写；> $100 退款触发挂起。

---

## P6 · 评估与可观测 ⬜

- [ ] 构建 100 条跨平台多语言仿真工单数据集
- [ ] Ragas 评估脚本（Context Recall / Faithfulness）
- [ ] 工具调用准确率 / 合规率 / P95 延迟指标采集
- [ ] Langfuse 接入（Trace / Token / Latency）
- [ ] CI 中跑评估并输出对比报告

**验收标准**：输出 README 中五项指标的实测数值并与基线对比。

---

## P7 · 前端与部署 ⬜

- [ ] Streamlit 多平台仿真控制台（4 个演示场景 + 人工审批）
- [ ] Dockerfile 多阶段构建
- [ ] `docker compose` 一键拉起 API + 前端 + PG + Redis + 向量库
- [ ] GitHub Actions：lint + test + 镜像构建

**验收标准**：`docker compose up` 后浏览器可完成一次端到端演示。

---

## 风险与依赖

| 风险 | 影响 | 应对 |
| :--- | :--- | :--- |
| LLM API 成本 / 限流 | 开发调试变慢 | 本地缓存 + mock LLM 模式 |
| 平台真实 API 权限申请周期长 | P2 阻塞 | 先 mock，接口按真实契约设计 |
| 向量库选型摇摆（Chroma vs Qdrant） | P4 返工 | P3 前定稿，封装 Repository 接口隔离 |
| HITL 状态恢复复杂 | P5 进度风险 | 先用内存 Saver 验证图逻辑，再切 Postgres |
| 评估集标注工作量 | P6 阻塞 | 复用仿真 Mock 数据半自动生成 |

---

## 里程碑

| 里程碑 | 包含阶段 | 交付物 |
| :--- | :--- | :--- |
| M1 可查询 | P0-P1 | 订单查询 API 可跑通 |
| M2 可对话 | P2-P3 | 仿真前端完成一次改地址闭环 |
| M3 可排障 | P4 | 多语言说明书问答 |
| M4 可上线 | P5-P7 | 护栏 + 人工台 + 部署包 |
