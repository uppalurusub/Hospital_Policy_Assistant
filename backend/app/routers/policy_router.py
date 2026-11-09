"""
==============================================================
File: policy_router.py

Description:
------------
FastAPI Router for Hospital Policy Assistant.

Architecture
------------
Client
    ↓
Router
    ↓
Service
    ↓
Implementation
    ↓
ChromaDB + LLM

Features
--------
✓ Upload Policy Documents
✓ Conversational RAG
✓ Session Memory
✓ Health Check
✓ Collection Statistics
✓ Reset Database
✓ Loguru Logging

Author: Your Name
==============================================================
"""

import shutil
from pathlib import Path
from typing import List, Optional
import os
from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from app.config.settings import settings
logger = settings.get_logger()

from app.schemas.request_model import PolicyQuestionRequest
from app.services.policy_service import policy_service

router = APIRouter(
    prefix="/policy",
    tags=["Hospital Policy Assistant"],
)

project_dir = Path(settings.project_dir)
UPLOAD_DIRECTORY = project_dir / "uploaded_documents"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

####################################################################
# Ask Question
####################################################################

@router.post(
    "/ask",
    summary="Ask Hospital Policy Questions"
)
async def ask_question(
    request: PolicyQuestionRequest,
):
    """
    Ask questions using Conversational RAG.
    """

    try:

        logger.info("=" * 80)
        logger.info("POST /policy/ask")

        response = policy_service.ask_question(request)

        logger.success("Question processed successfully.")

        return response

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )


####################################################################
# Upload Single Document
####################################################################

@router.post(
    "/upload",
    summary="Upload Policy Document"
)
async def upload_document(
    file: UploadFile = File(...),
    department: Optional[str] = Form("General"),
    document_type: Optional[str] = Form("Policy"),
    uploaded_by: Optional[str] = Form(None),
):
    """
    Upload one policy document.
    """

    try:

        logger.info("=" * 80)
        logger.info("POST /policy/upload")

        file_path = UPLOAD_DIRECTORY / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        metadata = {
            "department": department,
            "document_type": document_type,
            "uploaded_by": uploaded_by,
        }

        response = policy_service.upload_document(
            file_path=str(file_path),
            metadata=metadata,
        )

        logger.success("Document uploaded successfully.")

        return response

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )




####################################################################
# Clear Session Memory
####################################################################

@router.delete(
    "/memory/{session_id}",
    summary="Clear Conversation Memory"
)
async def clear_memory(
    session_id: str,
):
    """
    Clear one session.
    """

    try:

        logger.info(
            f"DELETE Memory : {session_id}"
        )

        return policy_service.clear_memory(
            session_id
        )

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )


####################################################################
# Clear All Memory
####################################################################

@router.delete(
    "/memory",
    summary="Clear All Memory"
)
async def clear_all_memory():
    """
    Clears all conversations.
    """

    try:

        logger.warning(
            "Deleting all memories."
        )

        return policy_service.clear_all_memory()

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )


####################################################################
# Health Check
####################################################################

@router.get(
    "/health",
    summary="Health Check"
)
async def health():
    """
    Application health.
    """

    try:

        logger.info(
            "GET /policy/health"
        )

        return policy_service.health()

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )


####################################################################
# Collection Statistics
####################################################################

@router.get(
    "/statistics",
    summary="Collection Statistics"
)
async def statistics():
    """
    Chroma statistics.
    """

    try:

        logger.info(
            "GET Collection Statistics"
        )

        return policy_service.collection_statistics()

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )


####################################################################
# Active Sessions
####################################################################

@router.get(
    "/sessions",
    summary="Active Sessions"
)
async def active_sessions():
    """
    Returns active session IDs.
    """

    try:

        logger.info(
            "GET Active Sessions"
        )

        return policy_service.active_sessions()

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )


####################################################################
# Reset Vector Database
####################################################################

@router.delete(
    "/database/reset",
    summary="Reset Chroma Database"
)
async def reset_database():
    """
    Deletes all indexed vectors.
    """

    try:

        logger.warning(
            "Reset Database Requested."
        )

        return policy_service.reset_database()

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )