from dotenv import load_dotenv
import os

load_dotenv()  # lee el .env

BASE_URL = os.getenv("BASE_URL")

