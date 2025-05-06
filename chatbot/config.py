import os
from dotenv import load_dotenv

load_dotenv()

JWS_KEY = os.getenv("JWS_KEY")
API_URL = os.getenv("API_URL")
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")