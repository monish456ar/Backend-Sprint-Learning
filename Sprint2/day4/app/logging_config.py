import contextvars
import json
import logging
import re
import sys
from datetime import datetime, timezone
from typing import Optional

# Request-scoped ContextVar to propagate request IDs across asynchronous calls
request_id_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "request_id", default=None
)

# Friendly mapping for internal library loggers
LOGGER_MAP = {
    "uvicorn.access": "http_access",
    "uvicorn.error": "http_server",
    "uvicorn": "http_server",
    "app.exception_handler": "exception_handler",
    "app.main": "app",
}


class StructuredJsonFormatter(logging.Formatter):
    """
    Formats log records as clean, structured JSON containing:
    - level: Log level string (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    - timestamp: ISO-8601 formatted UTC timestamp
    - logger: Meaningful component name (e.g. http_access, film_service, exception_handler)
    - message: Clean, human-readable log message
    - request_id: Attached request ID if present in context
    """

    def format(self, record: logging.LogRecord) -> str:
        raw_msg = record.getMessage()
        message = raw_msg

        # Format uvicorn access logs cleanly into human-readable descriptions
        if record.name == "uvicorn.access":
            if record.args and len(record.args) >= 5:
                # record.args = (client_addr, method, full_path, http_version, status_code)
                _, method, full_path, _, status_code = record.args[:5]
                message = f"HTTP {method} {full_path} -> {status_code}"
            else:
                match = re.search(r'"([A-Z]+)\s+([^"\s]+)[^"]*"\s+(\d+)', raw_msg)
                if match:
                    method, full_path, status_code = match.groups()
                    message = f"HTTP {method} {full_path} -> {status_code}"

        # Resolve clean, meaningful logger name
        logger_name = LOGGER_MAP.get(record.name, record.name.removeprefix("app."))

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        log_entry = {
            "level": record.levelname,
            "timestamp": timestamp,
            "logger": logger_name,
            "message": message,
        }

        # Attach request_id directly from ContextVar or record attribute
        req_id = getattr(record, "request_id", None) or request_id_ctx.get()
        if req_id:
            log_entry["request_id"] = req_id

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_logging(log_level: int = logging.INFO) -> None:
    """Configures structured JSON logging on root and application loggers."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredJsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid duplicating handlers if setup_logging is called multiple times
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)
    root_logger.addHandler(handler)

    # Ensure uvicorn and app loggers use the structured JSON formatter
    for logger_name in ("uvicorn", "uvicorn.error", "app"):
        l = logging.getLogger(logger_name)
        l.handlers = [handler]
        l.propagate = False

    # Mute default uvicorn.access so our request-scoped middleware logs it with request_id
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers = []
    uvicorn_access.propagate = False
    uvicorn_access.setLevel(logging.WARNING)
