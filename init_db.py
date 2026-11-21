import asyncio
from sqlalchemy import select
from app.core.database import engine, async_session
from app.models.base import Base
from app.models.order import Order

async def init_and_seed():
    print("⏳ 正在连接 MySQL 并建表...")
    async with engine.begin() as conn:
        # 扫描所有继承 Base 的模型并建表
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 表结构创建成功！")

    print("⏳ 正在插入测试数据...")
    async with async_session() as session:
        # 检查是否已经有数据
        result = await session.execute(select(Order))
        if result.scalars().first():
            print("⚠️ 数据库已有数据，跳过插入。")
            return

        # 插入假订单
        order1 = Order(
            order_id="ORD-1001",
            platform="amazon",
            customer_email_suffix="1234",
            status="delivered",
            paid_amount=99.99,
            currency="USD",
            items_summary="智能手表 * 1"
        )
        session.add(order1)
        await session.commit()
    print("✅ 数据插入成功！现在可以去刷新浏览器了。")

if __name__ == "__main__":
    asyncio.run(init_and_seed())