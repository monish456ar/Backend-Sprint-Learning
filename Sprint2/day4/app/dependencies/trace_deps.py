from uuid import uuid4
from fastapi import Header


def get_trace_id(x_trace_id: str | None = Header(default=None, alias="X-Trace-ID")) -> str:
    """Reads request trace identifier from X-Trace-ID header, generating one if absent."""
    return x_trace_id or str(uuid4())
