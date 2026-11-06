from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import redis

from app.api.tasks import router as tasks_router
from app.core.config import settings
from app.database import Base, engine
from app import models  # noqa: F401 - ensures models are registered


app = FastAPI(
    title="TaskFlow API",
    version="1.0.0",
    description="A task management API built for Docker learning.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Convenient for this learning MVP. We will replace this with Alembic migrations
# when we reach the database-migrations lesson.
Base.metadata.create_all(bind=engine)

app.include_router(tasks_router)


@app.get("/")
def root():
    return {"name": "TaskFlow API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/dependencies")
def dependency_health():
    result = {"api": "ok", "postgres": "unknown", "redis": "unknown"}
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        result["postgres"] = "ok"
    except Exception as exc:
        result["postgres"] = f"error: {type(exc).__name__}"

    try:
        client = redis.Redis.from_url(settings.redis_url, socket_connect_timeout=2)
        client.ping()
        result["redis"] = "ok"
    except Exception as exc:
        result["redis"] = f"error: {type(exc).__name__}"

    return result
