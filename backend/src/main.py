import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from .core.logging import setup_logging
from .db.redis import check_redis_connection, close_redis_connection

# setup logging
setup_logging(level="INFO", app_name="cifrar-chat")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await check_redis_connection()
    except Exception:
        raise
    yield
    # Cleanup on shutdown

    await close_redis_connection()


app = FastAPI(lifespan=lifespan, title="cifrar-chat", version=0.1)


@app.get("/health")
def check_health():
    return {"status": "ok"}
