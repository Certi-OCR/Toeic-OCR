from contextlib import asynccontextmanager
import logging
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.common.error import BaseErrorResponse, NotFound
from app.common.response import ErrorResponse
from app.core.db.db import close_db_connect, connect_and_init_db
from app.middlewares.auth import auth_guard
from app.routes import auth, history, ocr, record


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Connect to DB
    await connect_and_init_db()
    yield
    # Close connection to DB
    await close_db_connect()


app = FastAPI(
    title="TOEIC OCR API",
    description="API for extracting information from TOEIC uploaded image or URL",
    version="1.0.0",
    lifespan=app_lifespan,
)


@app.exception_handler(BaseErrorResponse)
async def http_exception_handler(request: Request, exc: BaseErrorResponse):
    logging.info(f"status: {exc.status_code}")
    return JSONResponse(
        content=jsonable_encoder(
            ErrorResponse(status_code=exc.status_code, message=exc.detail)
        ),
        status_code=exc.status_code,
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            ErrorResponse(
                status_code=422,
                message="Validation failed",
                detail=exc.errors(),
                body=exc.body,
            )
        ),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(AuthMiddleware)


app.include_router(ocr.router, prefix="/api/ocr", tags=["ocr"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(record.router, prefix="/api/record", tags=["record"])
app.include_router(history.router, prefix="/api/history", tags=["record"])


# @auth_guard
@app.get("/", include_in_schema=False)
async def documentation():
    return RedirectResponse("/docs")


@app.api_route("/{full_path:path}", include_in_schema=False)
async def all_routes(request: Request):
    raise NotFound(message="Route not found")


# app.add_middleware(ExceptionHandlerMiddleware)
