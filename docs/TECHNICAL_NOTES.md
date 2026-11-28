# 技术笔记

> 记录实现细节、选型依据、踩坑与命令速查。按主题分节，持续追加。

---

## 1. 环境与依赖

- 运行环境：Ubuntu 24.04（容器 / 虚拟机）+ Python 3.12，基础设施用 Docker Compose
- 依赖安装方式：`uv sync`（`uv.lock` 保证可复现）；避免裸 `pip install` 破坏锁文件
- 版本要求：见 `pyproject.toml`（`requires-python >= 3.12`）；Chroma 用容器内 1.5.9
- 特殊依赖：`pysqlite3-binary` —— 顶替系统过旧的 `libsqlite3`，详见第 4 节踩坑记录

---

## 2. 配置管理

- 配置项：
- 加载方式：
- 注意事项：

---

## 3. 核心实现要点

### 3.1 数据库

- 

### 3.2 模型 / 业务逻辑

- 

### 3.3 外部服务 / LLM

- 

---

## 4. 踩坑记录

| 现象 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| `import app.core.llm` 抛 `openai.OpenAIError: Missing credentials`，导致服务在未配置 LLM Key 时无法启动 | `llm.py` 在模块顶层实例化 `ChatOpenAI`，底层 openai 客户端构造时立即校验 `api_key`；`LLM_API_KEY` 默认值为空 | 改为 `@lru_cache` 装饰的 `get_llm()` 惰性工厂，构造前判空并抛中文 `RuntimeError`，使服务可在无 Key 时正常启动 |
| `import chromadb` 报 `undefined symbol: sqlite3_deserialize`；进一步发现连标准库 `import sqlite3` 本身都失败 | 系统 `libsqlite3` 过旧，缺少该符号（需 SQLite 3.23+），环境无 sudo 无法 `apt` 升级；chromadb 顶层 `import sqlite3` 连带失败 | `uv add pysqlite3-binary`（自带 SQLite 3.51.1），新增 `app/core/_sqlite_compat.py` 把 `sys.modules["sqlite3"]` 指向它，并在 `app/__init__.py` 最顶部触发 |

---

## 5. 常用命令

```bash
# 启动基础设施（PostgreSQL + Chroma）
docker compose up -d

# 建表并写入种子订单（ORD-1001）
.venv/bin/python init_db.py

# 启动 API（端口可自行指定）
.venv/bin/uvicorn app.main:app --reload --port 8000

# 验证接口
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/orders/ORD-1001

# 运行测试（测试用例待补充）
.venv/bin/python -m pytest
```

---

## 6. 待办 / 技术债

- [ ] 
- [ ] 
- [ ] 

---

## 7. 排障 CheckList

1. 
2. 
3. 
