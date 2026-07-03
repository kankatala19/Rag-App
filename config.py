from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DB_DIRECTORY = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "rag_documents"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")