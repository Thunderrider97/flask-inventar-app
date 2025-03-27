import os
from dotenv import load_dotenv
from pathlib import Path

# .env laden
basedir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=basedir / ".env")

#DB Verbindung
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
