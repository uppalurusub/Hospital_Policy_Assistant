"""
==============================================================
File: response_model.py

Description:
------------
Pydantic response models for Hospital Policy Assistant.

Features:
---------
- Question Answer Response
- Document Upload Response
- Memory Clear Response
- Health Check Response
- Standard API Response

Author: Your Name
==============================================================
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SourceDocument(BaseModel):
    """
    Information about the retrieved source document.
    """

    document_name: str = Field(
        ...,
        description="Name of the source document."
    )

    page_number: Optional[int] = Field(
        default=None,
        description="Page number from which the answer was retrieved."
    )

    section: Optional[str] = Field(
        default=None,
        description="Section heading in the document."
    )

    relevance_score: Optional[float] = Field(
        default=None,
        description="Retriever similarity score."
    )


class PolicyQuestionResponse(BaseModel):
    """
    Response returned after answering a policy question.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Answer generated successfully.",
                "question": "What is the leave approval process?",
                "answer": "Employees must submit leave requests through the HR portal and obtain approval from their reporting manager.",
                "conversation_id": "SESSION001",
                "language": "English",
                "sources": [
                    {
                        "document_name": "HR_Policy.pdf",
                        "page_number": 12,
                        "section": "Leave Policy",
                        "relevance_score": 0.95
                    }
                ],
                "timestamp": "2026-06-25T12:45:20"
            }
        }
    )

    success: bool = True

    message: str

    question: str

    answer: str

    conversation_id: str

    language: str

    sources: List[SourceDocument] = []

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class UploadResponse(BaseModel):
    """
    Response after uploading policy documents.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Document uploaded successfully.",
                "file_name": "Hospital_SOP.pdf",
                "chunks_created": 165,
                "collection_name": "hospital_policy"
            }
        }
    )

    success: bool = True

    message: str

    file_name: str

    chunks_created: int

    collection_name: str


class MemoryClearResponse(BaseModel):
    """
    Response after clearing conversation memory.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Conversation memory cleared successfully.",
                "session_id": "SESSION001"
            }
        }
    )

    success: bool = True

    message: str

    session_id: str


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "Healthy",
                "vector_store": "Connected",
                "llm": "Connected",
                "memory": "Available",
                "timestamp": "2026-06-25T12:50:10"
            }
        }
    )

    status: str

    vector_store: str

    llm: str

    memory: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "message": "Unable to process the request.",
                "error": "Vector store is not initialized."
            }
        }
    )

    success: bool = False

    message: str

    error: str