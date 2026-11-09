"""
==============================================================
File: conversation_memory.py

Description:
------------
Session-based conversation memory manager for
Hospital Policy Assistant.

Features
--------
- Session-based chat history
- Multi-user support
- Memory cleanup
- Conversation retrieval
- Thread-safe
- Loguru logging

Author: Your Name
==============================================================
"""

from threading import Lock
from typing import Dict

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from app.config.settings import settings
logger = settings.get_logger()


class ConversationMemory:
    """
    Manages session-wise chat history.
    """

    def __init__(self):
        logger.info("Initializing ConversationMemory...")

        self._store: Dict[str, BaseChatMessageHistory] = {}
        self._lock = Lock()

        logger.success("ConversationMemory initialized successfully.")

    ####################################################################
    # Get Memory
    ####################################################################

    def get_memory(self, session_id: str) -> BaseChatMessageHistory:
        """
        Returns chat history for a session.
        Creates one if it doesn't exist.
        """

        try:
            with self._lock:

                if session_id not in self._store:
                    logger.info(
                        f"Creating new conversation memory "
                        f"for session: {session_id}"
                    )

                    self._store[session_id] = InMemoryChatMessageHistory()

                logger.debug(
                    f"Returning memory for session: {session_id}"
                )

                return self._store[session_id]

        except Exception as ex:
            logger.exception(
                f"Error retrieving memory: {ex}"
            )
            raise

    ####################################################################
    # Clear Memory
    ####################################################################

    def clear_memory(self, session_id: str) -> bool:
        """
        Clears a specific session memory.
        """

        try:

            with self._lock:

                if session_id in self._store:

                    self._store[session_id].clear()

                    del self._store[session_id]

                    logger.success(
                        f"Conversation memory cleared "
                        f"for session: {session_id}"
                    )

                    return True

                logger.warning(
                    f"Session not found: {session_id}"
                )

                return False

        except Exception as ex:
            logger.exception(
                f"Error clearing memory: {ex}"
            )
            raise

    ####################################################################
    # Clear All
    ####################################################################

    def clear_all(self):
        """
        Clears all conversation memories.
        """

        try:

            with self._lock:

                self._store.clear()

                logger.success(
                    "All conversation memories cleared."
                )

        except Exception as ex:
            logger.exception(
                f"Error clearing all memories: {ex}"
            )
            raise

    ####################################################################
    # Get Active Sessions
    ####################################################################

    def get_active_sessions(self):
        """
        Returns active session IDs.
        """

        try:

            sessions = list(self._store.keys())

            logger.info(
                f"Active Sessions: {len(sessions)}"
            )

            return sessions

        except Exception as ex:
            logger.exception(
                f"Error retrieving active sessions: {ex}"
            )
            raise

    ####################################################################
    # Memory Exists
    ####################################################################

    def session_exists(self, session_id: str) -> bool:
        """
        Checks whether session memory exists.
        """

        exists = session_id in self._store

        logger.debug(
            f"Session '{session_id}' exists: {exists}"
        )

        return exists

    ####################################################################
    # Number of Messages
    ####################################################################

    def message_count(self, session_id: str) -> int:
        """
        Returns number of messages in a session.
        """

        try:

            if session_id not in self._store:
                return 0

            history = self._store[session_id]

            count = len(history.messages)

            logger.debug(
                f"Session '{session_id}' has {count} messages."
            )

            return count

        except Exception as ex:
            logger.exception(
                f"Error counting messages: {ex}"
            )
            raise


########################################################################
# Singleton Instance
########################################################################

conversation_memory = ConversationMemory()