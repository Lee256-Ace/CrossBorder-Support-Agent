from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# create_async_engine: 创建异步数据库引擎
# echo=False: 关闭 SQL 打印（开发时可设为 True，在终端看每条 SQL）
# pool_pre_ping=True: 从连接池取连接前，先 ping 一下确认还活着
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

# sessionmaker: 创建一个"会话工厂"
# class_=AsyncSession: 生成的是异步会话（可以 await）
# expire_on_commit=False: 提交后数据对象不失效，可以继续访问
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# FastAPI 依赖注入函数
# 用法：在 API 路由里写 `db: AsyncSession = Depends(get_db)`
# FastAPI 会自动调用这个函数，创建一个会话，传给 API 函数
# API 函数执行完后，会话自动关闭
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
