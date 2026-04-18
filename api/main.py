"""
BaristaIQ FastAPI backend.
Run with: uvicorn api.main:app --reload
Docs at: http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import orders, scheduler, metrics, config

app = FastAPI(
    title="BaristaIQ API",
    description="Barista Intelligence System — REST API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(scheduler.router, prefix="/schedule", tags=["Scheduler"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(config.router, prefix="/config", tags=["Config"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "BaristaIQ"}
