import logging
import time
from typing import Callable, Awaitable
import uvicorn

from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager

from .core.logging import setup_logging
from .db.redis import check_redis_connection, close_redis_connection
from .routes import room_router

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
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["x-process-time"] = str(process_time)
    logger.info(
        msg=f"method:{request.method} url:{request.url} took:{process_time:.2f}seconds to complete"
    )
    return response


# routes
app.include_router(room_router.Router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info", reload=True)
