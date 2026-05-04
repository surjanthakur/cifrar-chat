import logging
import time
from typing import Callable, Awaitable

from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager

from .core.logging import setup_logging
from .db.redis import check_redis_connection, close_redis_connection
from .routes import room_router


setup_logging(level="INFO", app_name="cifrar-chat")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Ensures Redis connection is available at startup and properly
    closed during application shutdown.
    """

    try:
        await check_redis_connection()
        yield
    except Exception as err:
        raise RuntimeError(f"error on startup app {err}")
    finally:
        close_redis_connection()


app = FastAPI(lifespan=lifespan, title="cifrar-chat", version="0.1")


@app.get("/health")
def check_health():
    """Health check endpoint to verify if the application is running."""
    return {"status": "ok"}


@app.middleware("http")
async def log_request(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Middleware to log the details and processing time of each HTTP request.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable[[Request], Awaitable[Response]]): Function to process the request and get a response.

    Returns:
        Response: The HTTP response with an added "x-process-time" header containing the processing duration.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["x-process-time"] = str(process_time)
    logger.info(
        msg=f"method:{request.method} url:{request.url} took:{process_time:.2f}seconds to complete"
    )
    return response


# app routers
app.include_router(room_router.Router, prefix="/api")
