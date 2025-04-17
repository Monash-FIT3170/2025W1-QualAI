import os
from dotenv import load_dotenv

load_dotenv()

JWS_KEY = os.getenv("JWS_KEY")
API_URL = os.getenv("API_URL")