from fastapi import status


class AppError(Exception):
    """Base class for expected application errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "app_error"
    message: str = "An application error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.message)
        if message:
            self.message = message


class EvaluationError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "evaluation_error"
    message = "Could not evaluate listing."


class InternalServiceError(AppError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "internal_service_error"
    message = "Internal service error."
