from typing import List, Dict, Any
import functools

# In‑memory log of query calls
QUERY_LOG: List[Dict[str, Any]] = []

def log_query(func):
    """Decorator that records the function name and arguments in ``QUERY_LOG``.
    Preserves function metadata via ``functools.wraps``.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        QUERY_LOG.append({
            "function": func.__name__,
            "args": args,
            "kwargs": kwargs,
        })
        return func(*args, **kwargs)
    return wrapper
