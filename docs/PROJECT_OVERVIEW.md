# 项目概述 · CrossBorder-Support-Agent

> 面向多平台跨境电商（Amazon / Shopify / Shopee·TikTok）的智能客服与订单自动化 Multi-Agent 系统。

---

## 1. 项目简介

跨境电商的售后场景中，平台规则、物流链路与合规红线高度割裂：Amazon 站内信禁止外部链接与联系方式，Shopify 允许通过 API 直接改单，Shopee/TikTok 存在 COD 拒收与多语种混说。传统的单体 Prompt 问答无法同时满足「查得准、改得对、不违规」三点。

本项目目标是构建一个基于 **LangGraph 状态机** 的通用 Multi-Agent 引擎，具备：

- **多平台统一接入**：适配器层屏蔽异构平台数据结构差异；
- **按平台隔离的 AI 权限**：运行时动态绑定可用工具，Amazon 物理剥离写操作；
- **Agentic RAG**：按 SKU 隔离的父子分块 + 混合检索 + 重排，杜绝说明书参数串台；
- **双重合规护栏**：正则硬拦截 + Policy LLM 反思重写，形成 Self-Correction 闭环；
- **人机协同**：高危工单通过 LangGraph `interrupt` 挂起，人工审批后恢复执行。

---

## 2. 目标用户与价值

| 角色 | 痛点 | 系统价值 |
| :--- | :--- | :--- |
| 跨境卖家运营 | 多店铺客服分散、回复慢 | 统一工作台，自动处理 60%+ 常规咨询 |
| 客服团队 | 平台规则复杂，易踩封号红线 | 合规护栏强拦截，违规率降至 0 |
| 售后/财务 | 退货挽损靠经验、算账耗时 | 阶梯式挽损模型自动给出最优方案 |
| 开发者 | 平台 API 异构、扩展成本高 | 适配器 + 统一标准模型，新增平台只需实现 Adapter |

---

## 3. 核心业务场景

1. **WISMO（Where Is My Order）**：跨国物流多段状态解析、清关滞留解释、DDP/DDU 关税说明。
2. **订单写操作**：Shopify 未发货订单改地址 / 取消 / 发补偿券（携带幂等键）。
3. **售后挽损谈判**：基于「货值 vs 逆向运费」算账，阶梯式部分退款或本地仓退货路由。
4. **产品故障排查**：PDF 说明书按 SKU 隔离检索，多语言分步排查（如德语 `Fehler E04`）。
5. **高危客诉熔断**：差评威胁、A-to-Z 索赔、超额退款触发人工接管。

---

## 4. 当前项目状态

**阶段：MVP-0（基础设施与订单查询骨架）**

已具备：

- FastAPI 异步应用入口与健康检查；
- PostgreSQL 异步连接（SQLAlchemy 2.x + asyncpg）；
- `Order` 数据模型与建表 / 种子数据脚本；
- 只读订单查询接口 `GET /api/orders/{order_id}`；
- Docker Compose 编排 PostgreSQL 与 Chroma；
- LiteLLM/OpenAI 兼容的 LLM 客户端初始化。

尚未实现（规划中）：

- 平台适配器层（`app/adapters/`）
- LangGraph 状态机与各 Agent 节点
- Agentic RAG 管道与知识库入库脚本
- 合规护栏规则引擎
- Human-in-the-loop 审批台
- Ragas 自动化评估集
- 管理员鉴权（配置项已预留，未落地接口）

> 详细差距对照见 [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)，架构细节见 [ARCHITECTURE.md](./ARCHITECTURE.md)。

---

## 5. 技术栈

### 5.1 已落地（代码中实际存在）

| 领域 | 技术 |
| :--- | :--- |
| 语言 | Python 3.12+ |
| Web 框架 | FastAPI + Uvicorn |
| ORM / 数据库 | SQLAlchemy 2.x（异步）+ asyncpg + PostgreSQL 16 |
| 向量库 | Chroma 1.5.x（容器） |
| Agent 框架 | LangGraph / LangChain（已安装，未接入业务） |
| LLM 客户端 | `langchain-openai`（OpenAI 兼容接口） |
| 配置 | pydantic-settings + `.env` |
| 容器化 | Docker Compose |
| 测试 | pytest + pytest-asyncio |

### 5.2 规划中（README 目标架构）

- Qdrant 混合检索、Rank-BM25、BGE-Reranker
- Redis（会话窗口记忆 / PII 映射 / 令牌桶限流）
- PostgreSQL 作为 LangGraph Checkpointer
- Langfuse（Trace / Token 监控）
- Ragas（评估）
- Streamlit（多平台仿真工作台）

> 注意：README 中写的是 Qdrant + Python 3.11，实际依赖为 Chroma + Python ≥3.12，以代码为准。

---

## 6. 快速开始

```bash
# 1. 安装依赖（推荐 uv，也可 pip install -e .）
uv sync

# 2. 启动基础设施（PostgreSQL + Chroma）
docker compose up -d

# 3. 建表并写入种子订单（ORD-1001）
python init_db.py

# 4. 启动 API
uvicorn app.main:app --reload --port 8000

# 5. 验证
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/orders/ORD-1001
```

环境变量（`.env`，参考 [config.py](../app/core/config.py)）：

```
DATABASE_URL=postgresql+asyncpg://app:app123@localhost:5432/crossborder
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

---

## 7. 文档索引

| 文档 | 说明 |
| :--- | :--- |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 分层架构、数据模型、API 契约、目标 Agent 拓扑 |
| [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) | 分阶段任务计划与验收标准 |
| [DEVELOPMENT_LOG.md](./DEVELOPMENT_LOG.md) | 每日开发日志（按天记录） |
| [TECHNICAL_NOTES.md](./TECHNICAL_NOTES.md) | 技术细节、踩坑记录、命令速查 |
