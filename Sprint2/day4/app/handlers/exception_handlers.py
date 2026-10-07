import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.domain_exceptions import (
    AccessDeniedException,
    DomainException,
    FilmAlreadyExistsError,
    FilmHasActiveReviewsError,
    FilmNotFoundError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    InvalidTokenError,
    MissingTokenError,
    ReviewAlreadyExistsError,
    ReviewNotFoundError,
    ReviewNotOwnerError,
    TokenExpiredError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

logger = logging.getLogger("app.exception_handler")


async def unauthorized_exception_handler(
    request: Request, exc: DomainException
) -> JSONResponse:
    logger.warning("Authentication failure: %s", exc.message)
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )



async def film_already_exists_handler(
    request: Request, exc: FilmAlreadyExistsError
) -> JSONResponse:
    logger.warning("Business rule violation: %s", exc.message)
    return JSONResponse(
        status_code=409,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def review_already_exists_handler(
    request: Request, exc: ReviewAlreadyExistsError
) -> JSONResponse:
    logger.warning("Business rule violation: %s", exc.message)
    return JSONResponse(
        status_code=409,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def film_has_active_reviews_handler(
    request: Request, exc: FilmHasActiveReviewsError
) -> JSONResponse:
    logger.warning("Business rule violation: %s", exc.message)
    return JSONResponse(
        status_code=409,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def review_not_owner_handler(
    request: Request, exc: ReviewNotOwnerError
) -> JSONResponse:
    logger.warning("Business rule violation: %s", exc.message)
    return JSONResponse(
        status_code=403,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def film_not_found_handler(
    request: Request, exc: FilmNotFoundError
) -> JSONResponse:
    logger.warning("Entity not found: %s", exc.message)
    return JSONResponse(
        status_code=404,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def review_not_found_handler(
    request: Request, exc: ReviewNotFoundError
) -> JSONResponse:
    logger.warning("Entity not found: %s", exc.message)
    return JSONResponse(
        status_code=404,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def user_not_found_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    logger.warning("Entity not found: %s", exc.message)
    return JSONResponse(
        status_code=404,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    logger.warning("Entity conflict: %s", exc.message)
    return JSONResponse(
        status_code=409,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def generic_domain_exception_handler(
    request: Request, exc: DomainException
) -> JSONResponse:
    logger.warning("Domain exception: %s", exc.message)
    return JSONResponse(
        status_code=400,
        content={
            "type": exc.error_type,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def access_denied_handler(
    request: Request, exc: AccessDeniedException
) -> JSONResponse:
    logger.warning("Access denied: %s", exc.message)
    return JSONResponse(
        status_code=403,
        content={
            "type": "access_denied",
            "message": exc.message,
            "role": exc.role,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers all centralized domain exception handlers with the FastAPI application."""
    app.add_exception_handler(AccessDeniedException, access_denied_handler)
    app.add_exception_handler(FilmAlreadyExistsError, film_already_exists_handler)
    app.add_exception_handler(ReviewAlreadyExistsError, review_already_exists_handler)
    app.add_exception_handler(FilmHasActiveReviewsError, film_has_active_reviews_handler)
    app.add_exception_handler(ReviewNotOwnerError, review_not_owner_handler)
    app.add_exception_handler(FilmNotFoundError, film_not_found_handler)
    app.add_exception_handler(ReviewNotFoundError, review_not_found_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
    app.add_exception_handler(InvalidCredentialsError, unauthorized_exception_handler)
    app.add_exception_handler(InvalidTokenError, unauthorized_exception_handler)
    app.add_exception_handler(MissingTokenError, unauthorized_exception_handler)
    app.add_exception_handler(TokenExpiredError, unauthorized_exception_handler)
    app.add_exception_handler(InvalidRefreshTokenError, unauthorized_exception_handler)
    app.add_exception_handler(DomainException, generic_domain_exception_handler)

