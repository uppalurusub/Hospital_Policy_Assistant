"""
==============================================================
File: policy_service.py

Description:
------------
Service layer for Hospital Policy Assistant.

Architecture:
-------------
Router
    ↓
PolicyService
    ↓
PolicyImplementation

Features
--------
✓ Question Answering
✓ Document Upload
✓ Memory Management
✓ Health Check
✓ Collection Statistics
✓ Reset Database
✓ Loguru Logging

Author: Your Name
==============================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from app.implementations.policy_impl import PolicyImplementation

import mlflow
from datetime import datetime
import time
import os
from langsmith import traceable

mlflow.set_tracking_uri(
    "http://localhost:5000"
)

mlflow.set_experiment(
    "Hospital_Policy_Assistant_Interface"
)
from app.config.settings import settings,MODEL,INPUT_PRICE_PER_1M,OUTPUT_PRICE_PER_1M,LLMUsageTracker

class PolicyService:
    """
    Service layer for Hospital Policy Assistant.
    """

    ####################################################################
    # Constructor
    ####################################################################

    def __init__(self):

        logger.info(
            "Initializing PolicyService..."
        )

        self.policy_impl = PolicyImplementation()

        logger.success(
            "PolicyService initialized successfully."
        )

    ####################################################################
    # Ask Question
    ####################################################################

    @traceable(
        name="hospital-policy-api-workflow",
        run_type="chain",
        tags=["healthcare", "hospital-policy", "fastapi", "rag"],
        metadata={"service": "PolicyService", "endpoint": "/policy/ask"},
    )
    def ask_question(
        self,
        request
    ):
        """
        Answer user questions using Conversational RAG.
        """

        start_time = datetime.now()
        start_ts = time.time()

        tracker = LLMUsageTracker(
            model=MODEL,
            input_price_per_1m=INPUT_PRICE_PER_1M,
            output_price_per_1m=OUTPUT_PRICE_PER_1M,
        )

        try:

            logger.info(
                "Processing ask_question request."
            )

            with mlflow.start_run(
                run_name=
                f"Hospital_Policy_Assistant_Ask_Question_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ):
                # Log to MLflow
                mlflow.log_param(
                    "start_time",
                    start_time.strftime("%Y-%m-%d %H:%M:%S")
                )
                mlflow.log_param(
                    "input_question",
                    str(getattr(request, "question", ""))[:500]
                )
                mlflow.set_tag("workflow", "hospital_policy_qa")
                mlflow.set_tag("llm_provider", "openrouter")
                mlflow.set_tag("llm_model", os.getenv("fallback_model_1", "unknown"))

                response = self.policy_impl.ask_question(

                    question=request.question,

                    language=request.language,

                    user_id=request.user_id,

                    session_id=request.session_id,
                    usage_tracker=tracker
                )
                # Extract actual LLM usage
                usage = tracker.as_dict()
            
                answer_text = getattr(response, "answer", "")
                mlflow.log_param("output_preview", str(answer_text)[:500])
                mlflow.set_tag(
                    "request_success",
                    str(getattr(response, "success", False)).lower()
                )

                mlflow.set_tag(
                    "source",
                    "FastAPI"
                )

                mlflow.set_tag(
                    "endpoint",
                    "policy/ask"
                )



                end_time = datetime.now()
                end_ts = time.time()

                execution_time = end_ts - start_ts

                mlflow.log_param(
                    "end_time",
                    end_time.strftime("%Y-%m-%d %H:%M:%S")
                )

                mlflow.log_metric(
                    "execution_time_seconds",
                    round(execution_time, 4)
                )

                logger.info(
                    f"LLM usage captured | "
                    f"model={usage['model']} | "
                    f"input_tokens={usage['input_tokens']} | "
                    f"output_tokens={usage['output_tokens']} | "
                    f"total_tokens={usage['total_tokens']} | "
                    f"input_cost_usd={usage['input_cost_usd']:.12f} | "
                    f"output_cost_usd={usage['output_cost_usd']:.12f} | "
                    f"total_cost_usd={usage['total_cost_usd']:.12f} | "
                    f"llm_call_count={usage['llm_call_count']} | "
                    f"usage_reported_call_count="
                    f"{usage['usage_reported_call_count']}"
                )

                # Log metrics to the active MLflow run.
                mlflow.log_metrics({

                    "input_tokens": usage["input_tokens"],
                    "output_tokens": usage["output_tokens"],
                    "total_tokens": usage["total_tokens"],

                    "input_cost_usd": usage["input_cost_usd"],
                    "output_cost_usd": usage["output_cost_usd"],
                    "total_cost_usd": usage["total_cost_usd"],

                    "llm_call_count": usage["llm_call_count"],

                    "usage_reported_call_count": (
                        usage["usage_reported_call_count"]
                    ),

                    "execution_time_seconds": execution_time,

                })
        
            return response

        except Exception as ex:

            logger.exception(
                f"Service Error : {ex}"
            )

            raise

    ####################################################################
    # Upload One Document
    ####################################################################

    def upload_document(
        self,
        file_path: str,
        metadata: dict | None = None
    ):
        """
        Upload one policy document.
        """

        try:

            logger.info(
                f"Uploading document : {file_path}"
            )

            return self.policy_impl.upload_policy_document(

                file_path=file_path,

                metadata=metadata
            )

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Upload Multiple Documents
    ####################################################################

    def upload_documents(
        self,
        file_paths: list[str]
    ):
        """
        Upload multiple documents.
        """

        try:

            logger.info(
                f"Uploading {len(file_paths)} documents."
            )

            return self.policy_impl.upload_policy_documents(
                file_paths
            )

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Clear Session Memory
    ####################################################################

    def clear_memory(
        self,
        session_id: str
    ):
        """
        Clears one session.
        """

        try:

            logger.info(
                f"Clearing memory : {session_id}"
            )

            return self.policy_impl.clear_memory(
                session_id
            )

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Clear All Memory
    ####################################################################

    def clear_all_memory(self):
        """
        Clears all conversation memory.
        """

        try:

            logger.warning(
                "Clearing all conversation memory."
            )

            return self.policy_impl.clear_all_memory()

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Health Check
    ####################################################################

    def health(self):
        """
        Returns application health.
        """

        try:

            logger.info(
                "Health check requested."
            )

            return self.policy_impl.health()

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Collection Statistics
    ####################################################################

    def collection_statistics(self):
        """
        Returns Chroma collection statistics.
        """

        try:

            logger.info(
                "Collection statistics requested."
            )

            return self.policy_impl.collection_statistics()

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Reset Database
    ####################################################################

    def reset_database(self):
        """
        Deletes all indexed vectors.
        """

        try:

            logger.warning(
                "Reset database requested."
            )

            return self.policy_impl.reset_database()

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Active Sessions
    ####################################################################

    def active_sessions(self):
        """
        Returns active sessions.
        """

        try:

            logger.info(
                "Retrieving active sessions."
            )

            return self.policy_impl.active_sessions()

        except Exception as ex:

            logger.exception(ex)

            raise


########################################################################
# Singleton Service Instance
########################################################################

policy_service = PolicyService()