"""
==============================================================
File: request_model.py

Description:
------------
Pydantic request models for Hospital Policy Assistant.

Features:
---------
- Upload Policy Documents
- Ask Questions
- Session-based Conversation
- Language Support
- Validation

Author: Your Name
==============================================================
"""

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PolicyQuestionRequest(BaseModel):
    """
    Request model for asking questions about hospital policies.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "What is the leave approval process?",
                "language": "English",
                "user_id": "EMP001",
                "session_id": "SESSION001"
            }
        }
    )

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="User's question related to hospital policies."
    )

    language: str = Field(
        default="English",
        description="Preferred response language."
    )

    user_id: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Unique employee/user identifier."
    )

    session_id: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Unique conversation session identifier."
    )


class MemoryClearRequest(BaseModel):
    """
    Request model for clearing a conversation memory.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "SESSION001"
            }
        }
    )

    session_id: str = Field(
        ...,
        description="Conversation session ID."
    )


class DocumentUploadRequest(BaseModel):
    """
    Metadata for uploaded hospital policy documents.

    Note:
    -----
    The actual file is received separately using FastAPI's UploadFile.
    This model stores additional metadata.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "department": "Human Resources",
                "document_type": "Policy",
                "uploaded_by": "EMP001",
                "language": "English"
            }
        }
    )

    department: Optional[str] = Field(
        default="General",
        description="Department owning the document."
    )

    document_type: Optional[str] = Field(
        default="Policy",
        description="Policy, SOP, Compliance, Manual, etc."
    )

    uploaded_by: Optional[str] = Field(
        default=None,
        description="Employee ID of uploader."
    )

    language: str = Field(
        default="English",
        description="Document language."
    )