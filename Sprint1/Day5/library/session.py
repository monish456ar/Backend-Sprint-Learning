"""Context manager for catalogue session management."""

from datetime import datetime
from types import TracebackType


class CatalogueSession:
    """Wrap a library catalogue session with setup on enter and cleanup on exit."""

    def __init__(self, session_name: str = "Library Catalogue Session") -> None:
        self.session_name = session_name
        self.start_time: datetime | None = None

    def __enter__(self):
        self.start_time = datetime.now()
        print("=" * 45)
        print(f"[SESSION START] {self.session_name} started.")
        print("=" * 45)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        print("\n" + "=" * 45)
        print(f"[SESSION CLEANUP] Performing cleanup for '{self.session_name}'...")
        if exc_type is not None:
            print(f"[SESSION EXIT] Finished with error: {exc_type.__name__}")
        else:
            print("[SESSION EXIT] Finished successfully.")
        print("=" * 45 + "\n")
        return False
