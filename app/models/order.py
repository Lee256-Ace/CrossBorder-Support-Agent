from sqlalchemy import String, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    platform: Mapped[str] = mapped_column(String(16))
    customer_email_suffix: Mapped[str] = mapped_column(String(8))
    status: Mapped[str] = mapped_column(String(16))
    paid_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(8), default="USD")
    items_summary: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())