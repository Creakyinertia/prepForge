from core.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    to_http_exception,
)


def test_to_http_exception_preserves_not_found_details():
    exc = to_http_exception(
        NotFoundError("Topic not found")
    )

    assert exc.status_code == 404
    assert exc.detail == "Topic not found"


def test_to_http_exception_preserves_conflict_status():
    exc = to_http_exception(
        ConflictError("Topic already exists")
    )

    assert exc.status_code == 409
    assert exc.detail == "Topic already exists"


def test_to_http_exception_preserves_authentication_status():
    exc = to_http_exception(
        AuthenticationError("Invalid token")
    )

    assert exc.status_code == 401
    assert exc.detail == "Invalid token"
