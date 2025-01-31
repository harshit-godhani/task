from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DB_URL = os.getenv("DATABASE_URL")
    SEC_KEY = os.getenv("SECRET_KEY")
    ALGO = os.getenv("ALORITHM")
    ACCESS_TOKEN_EXPIRE = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE = os.getenv("REFRESH_TOKEN_EXPIRE_DAY")











