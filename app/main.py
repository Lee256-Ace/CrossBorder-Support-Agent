from fastapi import FastAPI
from app.routers.orders import router as orders_router

app = FastAPI(title="CrossBorder AI Agent")
app.include_router(orders_router)

@app.get("/api/health")
def health():
    return {"ok": True}