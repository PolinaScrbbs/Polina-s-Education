import os
from dotenv import load_dotenv

os.environ.pop("DB_USER", None)
os.environ.pop("DB_PASSWORD", None)
os.environ.pop("DB_NAME", None)

os.environ.pop("DATABASE_URL", None)
os.environ.pop("SECRET_KEY", None)

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
SECRET_KEY = os.getenv("SECRET_KEY")