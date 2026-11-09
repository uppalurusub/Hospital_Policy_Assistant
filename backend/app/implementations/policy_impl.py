"""
==============================================================
File: policy_impl.py

Description:
------------
Business implementation for Hospital Policy Assistant.

Features
--------
✓ Conversational RAG
✓ History Aware Retriever
✓ Session Memory
✓ ChromaDB
✓ LangChain
✓ Loguru Logging

Author: Your Name
==============================================================
"""

from typing import Dict
import os
import time
from langsmith import traceable

from app.config.settings import settings,LLMUsageTracker
logger = settings.get_logger()


from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain
)

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_core.runnables.history import (
    RunnableWithMessageHistory
)

from app.memory.conversation_memory import conversation_memory

from app.prompts.policy_prompt import PolicyPrompt

from app.utils.vector_store import vector_store

from pathlib import Path

from app.schemas.response_model import (
    UploadResponse,
    SourceDocument,
    MemoryClearResponse,
    HealthResponse,
    ErrorResponse,
    PolicyQuestionResponse
)



class PolicyImplementation:
    """
    Hospital Policy Assistant Implementation.
    """

    ####################################################################
    # Constructor
    ####################################################################

    def __init__(self):

        logger.info(
            "Initializing Hospital Policy Assistant..."
        )

        ###############################################################

        self.vector_store = vector_store

        ###############################################################

        self.llm = settings.get_model_client()

        logger.success("LLM Initialized.")

        ###############################################################

        self.memory = conversation_memory

        ###############################################################

        logger.info(
            "Creating Retriever..."
        )

        self.retriever = self.vector_store.get_retriever(
            k=4
        )

        logger.success("Retriever created.")

        ###############################################################

        self.chain_cache: Dict = {}

        logger.success(
            "Hospital Policy Assistant Initialized."
        )

    ####################################################################
    # Clear Session Memory
    ####################################################################

    def clear_memory(
        self,
        session_id: str
    ):
        """
        Clears conversation memory for a specific session.

        Args:
            session_id (str): Session identifier.

        Returns:
            dict: Operation status.
        """

        try:

            logger.info("=" * 80)
            logger.info(
                f"Clearing conversation memory for Session: {session_id}"
            )

            ############################################################
            # Check if session exists
            ############################################################

            if not self.memory.session_exists(session_id):

                logger.warning(
                    f"Session '{session_id}' not found."
                )

                return {
                    "success": False,
                    "message": f"Session '{session_id}' does not exist."
                }

            ############################################################
            # Count messages before clearing
            ############################################################

            message_count = self.memory.message_count(
                session_id
            )

            logger.info(
                f"Messages in session: {message_count}"
            )

            ############################################################
            # Clear memory
            ############################################################

            self.memory.clear_memory(session_id)

            ############################################################
            # Remove cached chain (optional)
            ############################################################

            if hasattr(self, "chain_cache"):
                self.chain_cache.clear()

            logger.success(
                f"Conversation memory cleared for session '{session_id}'."
            )

            return {

                "success": True,

                "message": "Conversation memory cleared successfully.",

                "session_id": session_id,

                "messages_removed": message_count
            }

        except Exception as ex:

            logger.exception(
                f"Failed to clear memory: {ex}"
            )

            return {

                "success": False,

                "message": "Failed to clear conversation memory.",

                "error": str(ex)
            }

    ####################################################################
    # Reset Vector Database
    ####################################################################

    def reset_database(self):
        """
        Reset the Chroma vector database.

        Deletes all indexed vectors and recreates an empty collection.

        Returns:
            dict: Status of the reset operation.
        """

        try:

            logger.warning("=" * 80)
            logger.warning("Resetting Chroma Vector Database...")

            ############################################################
            # Reset Chroma Collection
            ############################################################

            self.vector_store.reset_collection()

            ############################################################
            # Clear Conversation Memory
            ############################################################

            self.memory.clear_all()

            ############################################################
            # Clear Cached Chains
            ############################################################

            if hasattr(self, "chain_cache"):
                self.chain_cache.clear()

            logger.success("Vector database reset successfully.")

            return {
                "success": True,
                "message": "Vector database has been reset successfully.",
                "collection_name": self.vector_store.collection_name
            }

        except Exception as ex:

            logger.exception(f"Failed to reset vector database: {ex}")

            return {
                "success": False,
                "message": "Failed to reset vector database.",
                "error": str(ex)
            }

    ####################################################################
    # Clear All Conversation Memory
    ####################################################################

    def clear_all_memory(self):
        """
        Clears all active conversation memories.

        Returns:
            dict: Status of the operation.
        """

        try:

            logger.warning("=" * 80)
            logger.warning("Clearing all conversation memory...")

            ############################################################
            # Get active sessions before clearing
            ############################################################

            sessions = self.memory.get_active_sessions()
            total_sessions = len(sessions)

            logger.info(
                f"Total active sessions before clearing: {total_sessions}"
            )

            ############################################################
            # Clear memory
            ############################################################

            self.memory.clear_all()

            logger.success(
                f"Successfully cleared {total_sessions} session(s)."
            )

            return {
                "success": True,
                "message": "All conversation memory cleared successfully.",
                "total_sessions_cleared": total_sessions
            }

        except Exception as ex:

            logger.exception(
                f"Failed to clear all conversation memory: {ex}"
            )

            return {
                "success": False,
                "message": "Failed to clear conversation memory.",
                "error": str(ex)
            }

    ####################################################################
    # Active Sessions
    ####################################################################

    def active_sessions(self) -> dict:
        """
        Returns all active conversation sessions.

        Returns:
            dict: Active session details.
        """

        try:

            logger.info("Fetching active sessions...")

            sessions = self.memory.get_active_sessions()

            response = {
                "success": True,
                "message": "Active sessions retrieved successfully.",
                "total_sessions": len(sessions),
                "sessions": sessions
            }

            logger.success(
                f"Retrieved {len(sessions)} active session(s)."
            )

            return response

        except Exception as ex:

            logger.exception(
                f"Failed to retrieve active sessions: {ex}"
            )

            return {
                "success": False,
                "message": "Unable to retrieve active sessions.",
                "error": str(ex)
            }


    ####################################################################
    # Collection Statistics
    ####################################################################

    def collection_statistics(self) -> dict:
        """
        Returns vector database statistics.
        """

        try:

            logger.info("Fetching collection statistics...")

            vector_health = self.vector_store.health()

            active_sessions = self.memory.get_active_sessions()

            stats = {
                "success": True,
                "collection_name": self.vector_store.collection_name,
                "persist_directory": self.vector_store.persist_directory,
                "document_chunks": self.vector_store.collection_count(),
                "active_sessions": len(active_sessions),
                "session_ids": active_sessions,
                "vector_store_status": vector_health.get("status", "Unknown")
            }

            logger.success("Collection statistics retrieved.")

            return stats

        except Exception as ex:

            logger.exception(f"Collection statistics failed: {ex}")

            return {
                "success": False,
                "message": "Unable to retrieve collection statistics.",
                "error": str(ex)
            }

    def health(self):
        try:

            logger.info("Running health check...")

            vector_health = self.vector_store.health()

            return HealthResponse(

                status="Healthy",

                vector_store=vector_health["status"],

                llm="Connected",

                memory="Available"

            )

        except Exception as ex:

            logger.exception(ex)

            return ErrorResponse(

                success=False,

                message="Health check failed.",

                error=str(ex)

            )

    ####################################################################
    # Create Conversational Chain
    ####################################################################

    def _create_chain(
        self,
        language: str = "English"
    ):
        """
        Creates conversational RAG chain.
        """

        logger.info(
            f"Creating chain ({language})..."
        )

        if language in self.chain_cache:

            logger.info(
                "Returning cached chain."
            )

            return self.chain_cache[language]

        ###############################################################
        # Prompt
        ###############################################################

        history_prompt = PolicyPrompt.get_history_prompt()

        qa_prompt = PolicyPrompt.get_qa_prompt(language)

        history_retriever = create_history_aware_retriever(

            llm=self.llm,

            retriever=self.retriever,

            prompt=history_prompt
        )

        document_chain = create_stuff_documents_chain(

            llm=self.llm,

            prompt=qa_prompt
        )

        logger.success(
            "Chain Created."
        )

        ###############################################################
        # Retrieval Chain
        ###############################################################

        rag_chain = create_retrieval_chain(

            history_retriever,

            document_chain
        )

        logger.success(
            "Retrieval Chain Created."
        )

        ###############################################################
        # Runnable With Message History
        ###############################################################

        conversational_chain = RunnableWithMessageHistory(

            runnable=rag_chain,

            get_session_history=self.memory.get_memory,

            input_messages_key="input",

            history_messages_key="chat_history",

            output_messages_key="answer"
        )

        ###############################################################

        self.chain_cache[language] = conversational_chain

        logger.success(
            "Conversational Chain Ready."
        )

        return conversational_chain
    
    ####################################################################
    # Ask Question
    ####################################################################

    @traceable(
        name="hospital-policy-rag",
        run_type="chain",
        tags=["healthcare", "hospital-policy", "rag", "openrouter"],
        metadata={"component": "policy_impl", "workflow": "conversational_rag"},
    )
    def ask_question(
        self,
        question: str,
        language: str,
        user_id: str,
        session_id: str,
        usage_tracker: LLMUsageTracker | None = None
    ):
        """
        Ask a question using Conversational RAG.

        Returns:
            PolicyQuestionResponse
        """

        request_started = time.perf_counter()
        try:

            logger.info("=" * 80)
            logger.info("Hospital Policy Assistant Request")
            logger.info(f"User ID      : {user_id}")
            logger.info(f"Session ID   : {session_id}")
            logger.info(f"Language     : {language}")
            logger.info(f"Question     : {question}")

            ############################################################

            chain = self._create_chain(language)

            ############################################################

            logger.info("Invoking Conversational RAG Chain...")
            invoke_config = {
                "run_name": "hospital-policy-conversational-rag",

                "tags": [
                    "healthcare",
                    "hospital-policy",
                    "rag",
                    "openrouter"
                ],

                "metadata": {
                    "workflow": "hospital_policy_qa",
                    "language": language,
                    "llm_model": settings.model
                },

                "configurable": {
                    "session_id": session_id
                },

                # Capture token usage from actual LLM invocations.
                "callbacks": (
                    [usage_tracker]
                    if usage_tracker is not None
                    else []
                )
            }

            result = chain.invoke(
                {
                    "input": question
                },
                config=invoke_config
            )

            logger.success("LLM Response Generated Successfully.")
            logger.info(
                "RAG chain completed | elapsed_seconds={:.3f}",
                time.perf_counter() - request_started,
            )

            ############################################################
            # Extract Answer
            ############################################################

            answer = result.get(
                "answer",
                "No answer generated."
            )

            ############################################################
            # Extract Source Documents
            ############################################################

            logger.info("Extracting source documents...")

            sources = self._extract_sources(result)

            logger.success(
                f"Retrieved {len(sources)} source documents."
            )

            ############################################################

            response = PolicyQuestionResponse(

                success=True,

                message="Answer generated successfully.",

                question=question,

                answer=answer,

                conversation_id=session_id,

                language=language,

                sources=sources
            )

            logger.success("Response object created.")

            return response

        except Exception as ex:

            logger.exception(
                f"Error while answering question : {ex}"
            )

            return ErrorResponse(

                success=False,

                message="Failed to process the request.",

                error=str(ex)
            )


    ####################################################################
    # Extract Sources
    ####################################################################

    def _extract_sources(
        self,
        result
    ):
        """
        Converts retrieved documents into
        SourceDocument response model.
        """

        try:

            documents = result.get(
                "context",
                []
            )

            logger.info(
                f"Retrieved {len(documents)} documents."
            )

            sources = []

            for document in documents:

                metadata = document.metadata

                source = SourceDocument(

                    document_name=metadata.get(
                        "source",
                        "Unknown Document"
                    ),

                    page_number=metadata.get(
                        "page",
                        None
                    ),

                    section=metadata.get(
                        "section",
                        None
                    ),

                    relevance_score=metadata.get(
                        "score",
                        None
                    )
                )

                sources.append(source)

            return sources

        except Exception as ex:

            logger.exception(
                f"Source extraction failed : {ex}"
            )

            return []
    
    ####################################################################
    # Upload Policy Documents
    ####################################################################

    def upload_policy_document(
        self,
        file_path: str,
        metadata: dict | None = None
    ):
        """
        Upload and index a hospital policy document.

        Supported:
            PDF
            DOCX
            TXT
        """

        try:

            logger.info("=" * 80)
            logger.info("Uploading Hospital Policy Document")
            logger.info(f"File : {file_path}")

            if not Path(file_path).exists():
                raise FileNotFoundError(
                    f"File not found : {file_path}"
                )

            chunks = self.vector_store.add_document(
                file_path=file_path,
                metadata=metadata
            )

            logger.success(
                f"Successfully indexed {chunks} chunks."
            )

            return UploadResponse(

                success=True,

                message="Document uploaded successfully.",

                file_name=Path(file_path).name,

                chunks_created=chunks,

                collection_name=self.vector_store.collection_name
            )

        except Exception as ex:

            logger.exception(
                f"Document upload failed : {ex}"
            )

            return ErrorResponse(

                success=False,

                message="Document upload failed.",

                error=str(ex)
            )