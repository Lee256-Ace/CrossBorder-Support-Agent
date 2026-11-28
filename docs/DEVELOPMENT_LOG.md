# 项目开发日志

> 记录规则：
>
> 1. 每天新增一条 `## Day X - YYYY-MM-DD`，**不覆盖历史记录**。
> 2. 编号连续递增，跨周不重置。
> 3. 遇到的问题必须写清「现象 → 原因 → 解决」，便于复盘。
> 4. 日志与代码提交保持同一天，避免事后补记。

***

## Day X - YYYY-MM-DD

### 1. 今日开发目标

- <br />

### 2. 今日完成内容

- \[ ]
- \[ ]
- \[ ]

### 3. 涉及的代码模块

- 文件：
- 修改内容：

### 4. 遇到的问题

**问题描述：**

**原因分析：**

**解决方案：**

### 5. 今日学习总结

- 新学到的技术：
- 理解的技术原理：
- 仍然不理解的地方：

### 6. 当前项目进度

- 已完成：
- 进行中：
- 未开始：

### 7. 明日开发计划

- \[ ]
- \[ ]

### 8. 今日 Git 提交记录

- Commit：
- 备注：

***

## Day 1 - 2026-11-16 \~ 2026-11-17

### 1. 开发目标

- 市场、行业分析，计划使用多个LLM模型（DeepSeek、KIMI、ChatGPT）完成需求分析编写项目大纲
- 配置初始环境：安装docker、uv、git、
- 创建GitHub仓库，命名为CorssBorder-Support-Agent 
- 配置Docker-compose文件
- <br />

### 2. 完成内容

- \[ ]
- \[ ]
- \[ ]

### 3. 涉及的代码模块

- 文件：
- 修改内容：

### 4. 遇到的问题

**问题描述：Windows开发需要下载dockerdesktop 同时需要在本机安装Linux镜像环境，配置起来相对麻烦，害怕对本机已安装的软件起冲突。**

**原因分析： **

**解决方案：使用虚拟机VMware安装ubuntu24.4.3进行项目编程。**

### 5. 今日学习总结

- 新学到的技术：
- 理解的技术原理：
- 仍然不理解的地方：

### 6. 当前项目进度

- 已完成：
- 进行中：
- 未开始：

### 7. 明日开发计划

- \[ ]
- \[ ]

### 8. 今日 Git 提交记录

- Commit：
- 备注：

***

## Day 2 - 2026-11-28

### 1. 开发目标

- 对现有项目做完整现状审查，确认真实架构与 README 规划之间的差距
- 执行阶段 0 基线加固：修复 LLM 客户端导入即崩溃、补齐 `.env.example`、修复 Chroma 无法导入的环境问题

### 2. 完成内容

- \[x] 输出项目审查报告：实际架构 / 已实现 / 未实现 / 问题清单 / 能否启动 / README 差异 / 推荐开发顺序 / 首个任务
- \[x] 改造 `app/core/llm.py`：模块级实例化 → `get_llm()` 惰性工厂（`lru_cache` 缓存 + 空 Key 友好报错）
- \[x] 新增 `.env.example`，与 `app/core/config.py` 的 10 个配置字段一一对应
- \[x] 修复 Chroma 环境：`uv add pysqlite3-binary` + 新增 `app/core/_sqlite_compat.py` 垫片，`sqlite3` 升级到 3.51.1，`chromadb` 端到端写入 / 检索验证通过
- \[x] 回归验证：无 LLM Key 时 FastAPI 仍可正常启动，`/api/health` 与 `/api/orders/{order_id}` 正常

### 3. 涉及的代码模块

- 文件：`app/core/llm.py`、`.env.example`（新增）、`app/core/_sqlite_compat.py`（新增）、`app/__init__.py`、`pyproject.toml`、`uv.lock`
- 修改内容：
  - `app/core/llm.py`：删除模块级 `llm` 单例，改为 `@lru_cache` 装饰的 `get_llm()`，实例化前校验 `LLM_API_KEY`
  - `app/core/_sqlite_compat.py`：将 `sys.modules["sqlite3"]` 指向 `pysqlite3`，兼容旧系统 `libsqlite3` 缺符号问题
  - `app/__init__.py`：最顶部 import 垫片，保证先于 `chromadb` 执行
  - `pyproject.toml` / `uv.lock`：新增依赖 `pysqlite3-binary>=0.5.4.post2`

### 4. 遇到的问题

**问题描述 1：** `import app.core.llm` 直接抛 `openai.OpenAIError: Missing credentials`，导致服务在未配置 LLM Key 时无法启动。

**原因分析：** `llm.py` 在模块顶层就执行 `ChatOpenAI(...)` 实例化，底层 openai 客户端在构造时会立即校验 `api_key`；当前 `LLM_API_KEY` 默认值为空字符串。只要有代码 import 该模块（后续接入 Agent 必然会），整个 FastAPI 启动就会失败，属于「假安全」。

**解决方案：** 改为 `@lru_cache(maxsize=1)` 装饰的 `get_llm()` 惰性工厂，仅在首次真正调用 LLM 时才构造客户端；构造前先判空并抛出带修复指引的中文 `RuntimeError`。

**问题描述 2：** `import chromadb` 失败，报错 `_sqlite3...so: undefined symbol: sqlite3_deserialize`；进一步验证发现连标准库 `import sqlite3` 本身都失败。

**原因分析：** 当前容器的系统 `libsqlite3` 版本过旧，缺少 `sqlite3_deserialize` 符号（SQLite 3.23+ 才有），而 Python 的 `_sqlite3` 扩展引用了该符号；环境无免密 sudo，无法 `apt` 升级系统库。`chromadb` 在其 `__init__.py` 顶层 `import sqlite3`，因此连带无法导入。

**解决方案：** `uv add pysqlite3-binary`（自带静态编译的新版 SQLite 3.51.1），编写 `app/core/_sqlite_compat.py` 把 `sys.modules["sqlite3"]` 替换为 `pysqlite3`，并在 `app/__init__.py` 最顶部触发——利用 Python 导入子模块前先执行父包 `__init__` 的机制，保证垫片先于 `chromadb` 运行。端到端验证：内存客户端建集合、写入、检索均正常。

### 5. 今日学习总结

- 新学到的技术：用 `pysqlite3-binary` 顶替系统旧 `sqlite3` 的兼容手法；用 `functools.lru_cache` 实现客户端单例与惰性初始化。
- 理解的技术原理：Python 包导入顺序——导入任何 `app.*` 子模块前会先执行 `app/__init__.py`，因此可在包入口做全局前置补丁；模块级实例化的副作用会把「运行时错误」放大成「导入即崩溃」。
- 仍然不理解的地方：Chroma 与 Qdrant 的最终选型权衡，留到 P3 前定稿。

### 6. 当前项目进度

- 已完成：项目审查；阶段 0 基线加固（`llm.py` 惰性加载、`.env.example`、Chroma 环境修复）
- 进行中：准备进入阶段 1 / P2——统一数据模型 schemas 层
- 未开始：平台适配器、LangGraph 状态机、RAG、Guardrails、HITL、Redis、Streamlit、评估

### 7. 明日开发计划

- \[ ] 阶段 1：`app/schemas/unified.py` 定义 `UnifiedOrder` / `UnifiedMessage` / `ShipmentEvent`（Pydantic v2）
- \[ ] 为 `orders` 路由接入 `response_model`，用统一模型替代裸 dict 返回

### 8. 今日 Git 提交记录

- Commit：当前目录尚未初始化 git 仓库，暂无提交
- 备注：本次改动文件为 `app/core/llm.py`、`.env.example`、`app/core/_sqlite_compat.py`、`app/__init__.py`、`pyproject.toml`、`uv.lock`
