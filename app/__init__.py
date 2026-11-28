# 必须最先执行：修复旧环境 libsqlite3 缺少 sqlite3_deserialize 符号导致
# 标准库 sqlite3 / chromadb 无法导入的问题。详见 app/core/_sqlite_compat.py。
from app.core import _sqlite_compat  # noqa: F401
