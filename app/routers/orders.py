from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.order import Order

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/{order_id}")
async def get_order_detail(order_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.order_id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return {
        "order_id": order.order_id,
        "status": order.status,
        "amount": float(order.paid_amount),
    }