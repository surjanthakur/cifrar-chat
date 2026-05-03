from fastapi import FastAPI
from .core.logging import setup_logging
import logging

setup_logging(level="INFO", app_name="cifrar-chat")

logger = logging.getLogger(__name__)

app = FastAPI(title="cifrar-chat", version=0.1)


@app.get("/health")
def check_health():
    return {"status": "ok"}
