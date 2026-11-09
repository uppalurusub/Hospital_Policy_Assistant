"""
==============================================================
File: main.py

Description:
------------
Entry point for Hospital Policy Assistant.

Features
--------
✓ FastAPI
✓ Loguru Logging
✓ CORS
✓ Router Registration
✓ Startup & Shutdown Events
✓ Global Exception Handling
✓ Request Logging
✓ Health Endpoint

Author: Your Name
==============================================================
"""

import sys
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
logger = settings.get_logger()

from app.routers.policy_router import router as policy_router


########################################################################
# Configure Loguru
########################################################################

LOG_DIRECTORY = Path(settings.log_dir)


logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

logger.add(
    LOG_DIRECTORY / "hospital_policy_assistant.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)


########################################################################
# FastAPI Application
########################################################################

app = FastAPI(

    title="Hospital Policy Assistant API",

    description="""
Conversational RAG API for answering Hospital Policy,
SOP, Compliance and HR document questions.
""",

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc",

    openapi_url="/openapi.json",
)


########################################################################
# Middleware
########################################################################

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


########################################################################
# Request Logging Middleware
########################################################################

@app.middleware("http")
async def log_requests(
    request: Request,
    call_next
):
    """
    Logs all HTTP requests.
    """

    start = time.time()

    logger.info(
        f"{request.method} {request.url.path}"
    )

    response = await call_next(request)

    duration = round(
        time.time() - start,
        3
    )

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"Status={response.status_code} "
        f"Duration={duration}s"
    )

    return response




########################################################################
# Global Exception Handler
########################################################################

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(exc)

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message": "Internal Server Error",

            "error": str(exc)
        }
    )


########################################################################
# Root Endpoint
########################################################################

@app.get("/", tags=["Root"])
async def root():

    logger.info("Root endpoint called.")

    return {

        "application": "Hospital Policy Assistant",

        "version": "1.0.0",

        "status": "Running"
    }


########################################################################
# Health Endpoint
########################################################################

@app.get("/health", tags=["Health"])
async def health():

    logger.info("Health endpoint called.")

    return {

        "status": "Healthy",

        "application": "Hospital Policy Assistant"
    }


########################################################################
# Register Routers
########################################################################

app.include_router(policy_router)


