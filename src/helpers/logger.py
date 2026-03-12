"""Structured logging with request/response details."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import requests


def setup_logger(name: str = "api_framework", level: int = logging.INFO) -> logging.Logger:
    """Create a configured logger with structured formatting."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger()


def log_request(method: str, url: str, **kwargs: object) -> float:
    """Log outgoing request details. Returns the start timestamp."""
    logger.info("→ %s %s", method.upper(), url)
    if headers := kwargs.get("headers"):
        safe = {k: ("***" if k.lower() == "authorization" else v) for k, v in headers.items()}
        logger.debug("  Headers: %s", safe)
    if kwargs.get("json"):
        logger.debug("  Body: %s", kwargs["json"])
    if kwargs.get("params"):
        logger.debug("  Params: %s", kwargs["params"])
    return time.perf_counter()


def log_response(response: requests.Response, start: float) -> None:
    """Log incoming response details with elapsed time."""
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "← %s %s [%d] %.0fms",
        response.request.method,
        response.url,
        response.status_code,
        elapsed_ms,
    )
    if response.status_code >= 400:
        logger.warning("  Response body: %s", response.text[:500])
