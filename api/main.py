"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import evaluate, sessions, operations, websocket

app = FastAPI(
    title="MathLang API",
    description="REST API for the MathLang mathematical expression language",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate.router, prefix="/api", tags=["evaluate"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(operations.router, prefix="/api/operations", tags=["operations"])
app.include_router(websocket.router, prefix="/api", tags=["websocket"])


@app.get("/")
async def root():
    """API root - health check."""
    return {"status": "ok", "service": "MathLang API"}
