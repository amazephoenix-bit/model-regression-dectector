from dotenv import load_dotenv
import os

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL")
HOST = os.getenv("OLLAMA_HOST")
