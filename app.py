import os
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from config import UPLOAD_FOLDER, DB_DIRECTORY
from vectorstore import VectorStoreManager
from rag import RAGPipeline

app = FastAPI(title="Simple RAG API")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

vector_manager = VectorStoreManager()
rag = RAGPipeline()


@app.get("/")
def home():
    return {
        "message": "Simple RAG API Running Successfully"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    try:

        extension = os.path.splitext(file.filename)[1].lower()

        allowed_extensions = [
            ".pdf",
            ".txt",
            ".docx",
            ".md"
        ]

        if extension not in allowed_extensions:

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Unsupported File Type"
                }
            )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        vector_manager.create_vector_store(file_path)

        return {
            "success": True,
            "message": "Document uploaded successfully."
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )


@app.get("/query")
def query(question: str):

    try:

        result = rag.ask_question(question)

        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )


@app.post("/clear")
def clear_database():

    try:

        vector_manager.release_store()
        rag.vector_manager.release_store()
        vector_manager.clear_store()

        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        return {
            "success": True,
            "message": "Database Cleared Successfully"
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )