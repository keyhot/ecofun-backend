import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", "8080"))
HOST = os.getenv("HOST", "localhost")
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")