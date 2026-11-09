"""
==============================================================
File: vector_store.py

Description:
------------
Chroma Vector Store Manager for Hospital Policy Assistant.

Features
--------
✓ Persistent ChromaDB
✓ PDF/DOCX/TXT Loader
✓ Recursive Text Splitter
✓ HuggingFace Embeddings
✓ Similarity Search
✓ Retriever
✓ Collection Statistics
✓ Delete Collection
✓ Loguru Logging

Author: Your Name
==============================================================
"""

from pathlib import Path
from typing import List, Optional

from langchain_chroma import Chroma

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document

from app.config.settings import settings
logger = settings.get_logger()

project_dir = Path(settings.project_dir)
persist_directory = project_dir / "chroma_db"

class VectorStore:
    """
    Chroma Vector Store Manager.
    """

    def __init__(
            self,
            persist_directory: str = persist_directory,
            collection_name: str = "hospital_policy"
    ):

        logger.info("Initializing Chroma Vector Store...")

        self.persist_directory = persist_directory
        self.collection_name = collection_name

        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_db = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding,
            persist_directory=self.persist_directory
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        logger.success("Vector Store initialized successfully.")

    ####################################################################
    # Load Document
    ####################################################################

    def _load_document(self, file_path: str):

        extension = Path(file_path).suffix.lower()

        logger.info(f"Loading document : {file_path}")

        if extension == ".pdf":
            loader = PyPDFLoader(file_path)

        elif extension == ".docx":
            loader = Docx2txtLoader(file_path)

        elif extension == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")

        else:
            logger.error(f"Unsupported file type : {extension}")
            raise ValueError(f"Unsupported file type : {extension}")

        documents = loader.load()

        logger.info(f"Loaded {len(documents)} pages.")

        return documents

    ####################################################################
    # Add Document
    ####################################################################

    def add_document(
            self,
            file_path: str,
            metadata: Optional[dict] = None
    ) -> int:

        try:

            logger.info(f"Processing {file_path}")

            docs = self._load_document(file_path)

            chunks = self.text_splitter.split_documents(docs)

            logger.info(f"Generated {len(chunks)} chunks.")

            if metadata:

                for chunk in chunks:
                    chunk.metadata.update(metadata)

            self.vector_db.add_documents(chunks)

            logger.success(
                f"{len(chunks)} chunks stored successfully."
            )

            return len(chunks)

        except Exception as ex:

            logger.exception(f"Error adding document : {ex}")
            raise

    ####################################################################
    # Add Multiple Documents
    ####################################################################

    def add_documents(
            self,
            file_paths: List[str]
    ) -> int:

        total = 0

        for path in file_paths:

            total += self.add_document(path)

        logger.success(f"Total chunks indexed : {total}")

        return total

    ####################################################################
    # Similarity Search
    ####################################################################

    def similarity_search(
            self,
            query: str,
            k: int = 4
    ) -> List[Document]:

        logger.info(f"Searching documents for : {query}")

        docs = self.vector_db.similarity_search(
            query=query,
            k=k
        )

        logger.success(f"Retrieved {len(docs)} documents.")

        return docs

    ####################################################################
    # Similarity Search with Score
    ####################################################################

    def similarity_search_with_score(
            self,
            query: str,
            k: int = 4
    ):

        logger.info(
            f"Searching documents with similarity score."
        )

        return self.vector_db.similarity_search_with_score(
            query=query,
            k=k
        )

    ####################################################################
    # Retriever
    ####################################################################

    def get_retriever(
            self,
            k: int = 4
    ):

        logger.info("Creating retriever.")

        return self.vector_db.as_retriever(

            search_type="similarity",

            search_kwargs={
                "k": k
            }
        )

    ####################################################################
    # Collection Count
    ####################################################################

    def collection_count(self) -> int:

        try:

            collection = self.vector_db._collection

            count = collection.count()

            logger.info(
                f"Collection contains {count} vectors."
            )

            return count

        except Exception as ex:

            logger.exception(ex)
            return 0

    ####################################################################
    # Delete Collection
    ####################################################################

    def delete_collection(self):

        try:

            logger.warning(
                f"Deleting collection : {self.collection_name}"
            )

            self.vector_db.delete_collection()

            logger.success("Collection deleted.")

        except Exception as ex:

            logger.exception(ex)
            raise

    ####################################################################
    # Reset Collection
    ####################################################################

    def reset_collection(self):

        self.delete_collection()

        self.vector_db = Chroma(

            collection_name=self.collection_name,

            embedding_function=self.embedding,

            persist_directory=self.persist_directory
        )

        logger.success("Collection recreated.")

    ####################################################################
    # Health Check
    ####################################################################

    def health(self):

        try:

            count = self.collection_count()

            return {
                "status": "Healthy",
                "collection_name": self.collection_name,
                "persist_directory": self.persist_directory,
                "documents": count
            }

        except Exception as ex:

            logger.exception(ex)

            return {
                "status": "Unhealthy",
                "error": str(ex)
            }


########################################################################
# Singleton
########################################################################

vector_store = VectorStore()