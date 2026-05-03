import logging
import logging.config
from typing import Any, Optional
from __future__ import annotations


def setup_logging(*, level: str = "INFO", app_name: Optional[str] = None) -> None:
    """
    Configure Python logging once for the whole app.

    Usage: call this once at startup (e.g. in `src/main.py`).
    After that, in any file:
      import logging
      logger = logging.getLogger(__name__)
    """
    normalized_level = (level or "INFO").upper()
    logger_name_prefix = f"{app_name}." if app_name else ""

    config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": normalized_level,
                "formatter": "default",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": normalized_level,
            "handlers": ["console"],
        },
        "loggers": {
            # quiet noisy libraries if needed later
            f"{logger_name_prefix}": {"level": normalized_level},
        },
    }

    logging.config.dictConfig(config)
