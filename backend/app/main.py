import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import AppError
from app.routes.analyze import router as analyze_router
from app.middleware.logging import RequestLoggingMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flipsensei")

app = FastAPI(
    title="FlipSensei API",
    description="Backend service for FlipSensei listing analysis",
    version="0.1.0",
)

app.add_middleware(RequestLoggingMiddleware)


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    # Expected errors: return clean error payload
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Unexpected errors: log for debugging, return generic message
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={
            "error": {"code": "internal_error", "message": "Unexpected server error."}
        },
    )


app.include_router(analyze_router, prefix="/analyze", tags=["analyze"])
