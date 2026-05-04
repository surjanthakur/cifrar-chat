import logging
import time
from typing import Callable, Awaitable

from fastapi import FastAPI, Request, Response
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


@app.middleware("http")
async def log_request(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.time()
    response = call_next(request)
    process_time = time.time() - start_time
    Response.headers["x-process-time"] = str(process_time)
    logger.info(
        msg=f"method:{request.method} url: {request.url} time:{process_time:.2f}seconds"
    )
    return response
