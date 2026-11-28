"""旧系统 libsqlite3 兼容垫片。

背景：
    当前运行环境的系统 ``libsqlite3`` 版本过旧，缺少 ``sqlite3_deserialize``
    符号（该符号在 SQLite 3.23+ 才提供）。这会导致 Python 标准库 ``sqlite3``
    模块在导入时抛出：

        ImportError: .../_sqlite3...so: undefined symbol: sqlite3_deserialize

    而 ``chromadb`` 在其 ``__init__.py`` 顶层就 ``import sqlite3``，于是
    连带无法导入。由于当前环境无免密 sudo，不能升级系统库，故采用应用层替换。

做法：
    ``pysqlite3-binary`` 自带了一个较新版本的静态编译 SQLite。这里把它注册到
    ``sys.modules["sqlite3"]``，顶替标准库实现，使所有下游 ``import sqlite3``
    （包括 Chroma 内部）都拿到可用的客户端。

    本模块必须在 **任何** ``import sqlite3`` / ``import chromadb`` 之前执行。
    为此它在 ``app/__init__.py`` 的最顶部被导入——Python 导入子模块前会先执行
    父包 ``__init__``，从而保证垫片先于业务代码运行。
"""

import sys

try:
    import pysqlite3  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - 仅当依赖未安装时触发
    pysqlite3 = None  # type: ignore[assignment]

if pysqlite3 is not None:
    # 直接赋值（而非 setdefault）：若此前有残缺的 sqlite3 条目，也要覆盖掉
    sys.modules["sqlite3"] = pysqlite3
