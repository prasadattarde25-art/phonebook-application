import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routes import router
from .database import Base, engine
from . import models


# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Phonebook API",
    description="A production-ready REST API for managing contacts",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Request Logging Middleware
# --------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(
        "Request started: %s %s",
        request.method,
        request.url.path
    )

    response = await call_next(request)

    logger.info(
        "Request completed: %s %s - Status: %s",
        request.method,
        request.url.path,
        response.status_code
    )

    return response


# --------------------------------------------------
# Global Exception Handler
# --------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        "Unhandled error on %s %s: %s",
        request.method,
        request.url.path,
        str(exc)
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "phonebook-api"
    }


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/", tags=["Health"])
def home():
    return {
        "message": "Phonebook API is running"
    }


# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(router)