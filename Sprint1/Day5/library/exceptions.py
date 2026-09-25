"""Custom domain exceptions for the library catalogue system."""

from typing import Any


class LibraryException(Exception):
    """Base exception for all library catalogue domain errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message


class ResourceNotFoundError(LibraryException):
    """Raised when a requested resource (book, member, loan) cannot be found."""

    def __init__(self, resource_type: str, resource_id: str) -> None:
        self.resource_type: str = resource_type
        self.resource_id: str = resource_id
        message = f"{resource_type.capitalize()} with ID/ISBN '{resource_id}' was not found in the catalogue."
        super().__init__(message)


class InvalidInputError(LibraryException):
    """Raised when input data is invalid (e.g., negative fine rate, empty strings)."""

    def __init__(self, field: str, value: Any, reason: str) -> None:
        self.field: str = field
        self.value: Any = value
        self.reason: str = reason
        message = f"Invalid value for field '{field}' ({value!r}): {reason}"
        super().__init__(message)
