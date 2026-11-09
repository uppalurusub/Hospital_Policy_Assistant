"""
==============================================================
File: policy_prompt.py

Description:
------------
Prompt template for Hospital Policy Assistant.

Features
--------
✓ Conversational RAG
✓ Context-aware responses
✓ Chat history support
✓ Multi-language responses
✓ Hallucination prevention
✓ Source-based answers
✓ Loguru logging

Author: Your Name
==============================================================
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.config.settings import settings
logger = settings.get_logger()


class PolicyPrompt:
    """
    Generates prompt templates for Hospital Policy Assistant.
    """

    @staticmethod
    def get_history_prompt():

        return ChatPromptTemplate.from_messages(
        [

            (
                "system",

                """
Given the conversation and the latest user question,
rewrite the question so it can be understood without
chat history.

Do NOT answer the question.
Return only the rewritten question.
"""
            ),

            MessagesPlaceholder("chat_history"),

            (
                "human",

                "{input}"
            )

        ]
    )

    @staticmethod
    def get_qa_prompt(language):

        return ChatPromptTemplate.from_messages(
        [

            (
                "system",

                f"""
You are a Hospital Policy Assistant.

Answer ONLY from the retrieved context.

Context:

{{context}}

If answer not found say

The information is not available in the uploaded documents.

Respond in {language}.
"""
            ),

            MessagesPlaceholder("chat_history"),

            (
                "human",

                "{input}"
            )

        ]
    )

    @staticmethod
    def get_system_prompt(language: str = "English") -> str:
        """
        Returns the system prompt.
        """

        logger.info(
            f"Generating system prompt for language: {language}"
        )

        return f"""
You are an Expert Hospital Policy Assistant.

Your responsibility is to answer ONLY using the retrieved hospital
documents provided in the context.

--------------------------------------------------------
Supported Documents
--------------------------------------------------------

• Hospital SOPs
• HR Policies
• Nursing Policies
• Infection Control Guidelines
• Pharmacy Policies
• Quality Manuals
• Compliance Documents
• NABH/JCI Guidelines
• Emergency Procedures

--------------------------------------------------------
Instructions
--------------------------------------------------------

1. Answer ONLY using the retrieved context.

2. Never use outside knowledge.

3. Never hallucinate.

4. If the answer cannot be found in the provided context, respond exactly:

"The provided hospital policy documents do not contain enough information to answer this question."

5. If multiple documents provide relevant information, summarize them clearly.

6. Quote the document name, section heading, or page number whenever available.

7. Use previous conversation only to understand follow-up questions.
Do NOT use chat history as factual evidence unless it is supported by
the retrieved context.

8. If the question is unrelated to hospital policies or procedures,
respond politely:

"I can only answer questions related to the uploaded hospital policy documents."

9. Respond in **{language}**.

10. Keep answers:
    • Accurate
    • Professional
    • Concise
    • Easy to understand

11. If the user asks for a step-by-step procedure, provide numbered steps
only if they are explicitly available in the retrieved documents.

12. Do not make assumptions or infer missing policy details.

--------------------------------------------------------
Response Format
--------------------------------------------------------

Answer:

Sources:
- Document:
- Section:
- Page:

--------------------------------------------------------
Retrieved Context
--------------------------------------------------------

{{context}}
"""

    @classmethod
    def get_chat_prompt(cls, language: str = "English") -> ChatPromptTemplate:
        """
        Returns a ChatPromptTemplate for Conversational RAG.
        """

        logger.info("Creating ChatPromptTemplate...")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    cls.get_system_prompt(language),
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    "{input}",
                ),
            ]
        )

        logger.success("ChatPromptTemplate created successfully.")

        return prompt