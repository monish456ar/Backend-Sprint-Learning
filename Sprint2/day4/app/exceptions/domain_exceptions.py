"""
Domain Exceptions for the Film Review Platform.

These exceptions represent business logic and entity domain failures,
keeping the DAO and Service layers independent from HTTP/FastAPI concerns.
"""

from typing import Any, Optional


class DomainException(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(
        self,
        message: str,
        detail: Optional[str] = None,
        error_type: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or message
        self.error_type = error_type or self.__class__.__name__.removesuffix("Error")


class FilmNotFoundError(DomainException):
    """Raised when a requested Film cannot be found in the database."""

    def __init__(self, film_id: Any, detail: Optional[str] = None) -> None:
        self.film_id = film_id
        super().__init__(
            message=f"Film with id {film_id} not found.",
            detail=detail or f"Film with ID {film_id} does not exist.",
            error_type="FilmNotFound",
        )


class FilmAlreadyExistsError(DomainException):
    """Raised when attempting to create a Film with a title that already exists."""

    def __init__(self, title: str, detail: Optional[str] = None) -> None:
        self.title = title
        super().__init__(
            message=f"Film with title '{title}' already exists.",
            detail=detail or f"A film with the title '{title}' already exists in the platform.",
            error_type="FilmAlreadyExists",
        )


class ReviewNotFoundError(DomainException):
    """Raised when a requested Review cannot be found in the database."""

    def __init__(self, review_id: Any, detail: Optional[str] = None) -> None:
        self.review_id = review_id
        super().__init__(
            message=f"Review with id {review_id} not found.",
            detail=detail or f"Review with ID {review_id} does not exist.",
            error_type="ReviewNotFound",
        )


class UserNotFoundError(DomainException):
    """Raised when a requested User cannot be found in the database."""

    def __init__(self, identifier: str, detail: Optional[str] = None) -> None:
        self.identifier = identifier
        super().__init__(
            message=f"User '{identifier}' not found.",
            detail=detail or f"User '{identifier}' does not exist.",
            error_type="UserNotFound",
        )


class UserAlreadyExistsError(DomainException):
    """Raised when trying to create a User with an email or username that already exists."""

    def __init__(
        self, field: str, value: str, detail: Optional[str] = None
    ) -> None:
        self.field = field
        self.value = value
        super().__init__(
            message=f"User with {field} '{value}' already exists.",
            detail=detail or f"A user with this {field} already exists.",
            error_type="UserAlreadyExists",
        )


class ReviewAlreadyExistsError(DomainException):
    """Raised when a user attempts to submit a second review for the same film."""

    def __init__(
        self, user_id: Any, film_id: Any, detail: Optional[str] = None
    ) -> None:
        self.user_id = user_id
        self.film_id = film_id
        super().__init__(
            message=f"User {user_id} has already reviewed film {film_id}.",
            detail=detail or "User has already reviewed this film.",
            error_type="ReviewAlreadyExists",
        )


class ReviewNotOwnerError(DomainException):
    """Raised when a user attempts to modify a review they do not own."""

    def __init__(
        self, review_id: Any, user_id: Any, detail: Optional[str] = None
    ) -> None:
        self.review_id = review_id
        self.user_id = user_id
        super().__init__(
            message=f"User {user_id} is not the owner of review {review_id}.",
            detail=detail or "Only the review owner can update this review.",
            error_type="ReviewNotOwner",
        )


class FilmHasActiveReviewsError(DomainException):
    """Raised when an attempt is made to soft-delete a film that still has active reviews."""

    def __init__(
        self,
        film_id: Any,
        active_review_count: int = 1,
        detail: Optional[str] = None,
    ) -> None:
        self.film_id = film_id
        self.active_review_count = active_review_count
        super().__init__(
            message=f"Cannot soft delete film {film_id} because it has active reviews.",
            detail=detail
            or f"Film has {active_review_count} active review(s). Remove reviews before soft deleting the film.",
            error_type="FilmHasActiveReviews",
        )


class InvalidCredentialsError(DomainException):
    """Raised when invalid login credentials are provided."""

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(
            message="Invalid username or password.",
            detail=detail or "Could not validate credentials with provided username and password.",
            error_type="InvalidCredentials",
        )


class InvalidTokenError(DomainException):
    """Raised when a JWT token is invalid, malformed, or missing required claims."""

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(
            message="Could not validate credentials.",
            detail=detail or "Authentication token is invalid or malformed.",
            error_type="InvalidToken",
        )


class TokenExpiredError(DomainException):
    """Raised when a JWT token has expired."""

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(
            message="Token has expired.",
            detail=detail or "Authentication token has expired. Please log in again or refresh your token.",
            error_type="TokenExpired",
        )


class InvalidRefreshTokenError(DomainException):
    """Raised when an invalid or non-refresh token is submitted to the refresh endpoint."""

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(
            message="Invalid refresh token.",
            detail=detail or "Provided token is not a valid refresh token.",
            error_type="InvalidRefreshToken",
        )


class MissingTokenError(DomainException):
    """Raised when an Authorization header or token is missing from a protected request."""

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(
            message="Missing authorization token.",
            detail=detail or "Missing Authorization header. Please pass your token in the Authorization header.",
            error_type="MissingToken",
        )


class AccessDeniedException(Exception):
    """Raised when an authenticated user does not have the required role for an operation."""

    def __init__(self, role: str):
        self.role = role
        self.message = f"Access denied. Your role '{role}' is not allowed."
        super().__init__(self.message)

