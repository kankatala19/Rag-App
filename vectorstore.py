import gc
import os
import shutil
import time

from config import OPENAI_API_KEY, DB_DIRECTORY, COLLECTION_NAME

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


def _safe_remove_directory(path, max_retries=5):

    if not os.path.exists(path):
        return

    for attempt in range(max_retries):
        try:
            gc.collect()
            shutil.rmtree(path)
            return
        except PermissionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.3 * (attempt + 1))


class VectorStoreManager:

    def __init__(self):

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=OPENAI_API_KEY
        )
        self._vector_db = None

    def _open_chroma(self):

        return Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=DB_DIRECTORY,
            embedding_function=self.embeddings,
        )

    def release_store(self):

        if self._vector_db is not None:
            try:
                self._vector_db.delete_collection()
            except Exception:
                pass
            self._vector_db = None

        if os.path.exists(DB_DIRECTORY):
            try:
                vector_db = self._open_chroma()
                vector_db.delete_collection()
            except Exception:
                pass

        try:
            from chromadb.api.shared_system_client import SharedSystemClient

            SharedSystemClient.clear_system_cache()
        except Exception:
            pass

        gc.collect()

    def clear_store(self):

        self.release_store()
        _safe_remove_directory(DB_DIRECTORY)
        os.makedirs(DB_DIRECTORY, exist_ok=True)
        self._vector_db = None

    def load_document(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            documents = self._load_pdf(file_path)

        elif extension in {".txt", ".md"}:
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()

        elif extension == ".docx":
            loader = Docx2txtLoader(file_path)
            documents = loader.load()

        else:
            raise Exception("Unsupported File Type")

        documents = [
            doc for doc in documents
            if doc.page_content and doc.page_content.strip()
        ]

        if not documents:
            raise Exception(
                "No readable text found in the document. "
                "Scanned PDFs or image-only files are not supported."
            )

        return documents

    def _load_pdf(self, file_path):

        try:
            from langchain_community.document_loaders import PyMuPDFLoader

            loader = PyMuPDFLoader(file_path)
            documents = loader.load()
            if documents:
                return documents
        except Exception:
            pass

        loader = PyPDFLoader(file_path)
        return loader.load()

    def create_vector_store(self, file_path):

        documents = self.load_document(file_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            length_function=len,
        )

        chunks = splitter.split_documents(documents)

        chunks = [
            chunk for chunk in chunks
            if chunk.page_content and chunk.page_content.strip()
        ]

        print("=" * 60)
        print(f"Documents : {len(documents)}")
        print(f"Chunks    : {len(chunks)}")
        print("=" * 60)

        if not chunks:
            raise Exception("Document has no usable text after processing.")

        self.release_store()
        _safe_remove_directory(DB_DIRECTORY)
        os.makedirs(DB_DIRECTORY, exist_ok=True)

        vector_db = self._open_chroma()

        vector_db.add_documents(chunks)

        stored_count = vector_db._collection.count()
        if stored_count == 0:
            raise Exception(
                "Failed to store document in the vector database. Please try again."
            )

        print(f"Vector Database Created Successfully ({stored_count} chunks)")

        self._vector_db = vector_db

        return vector_db

    def load_vector_store(self):

        if not os.path.exists(DB_DIRECTORY):
            return None

        if self._vector_db is not None:
            if self._vector_db._collection.count() == 0:
                return None
            return self._vector_db

        vector_db = self._open_chroma()

        if vector_db._collection.count() == 0:
            return None

        self._vector_db = vector_db

        return vector_db
