from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from dotenv import load_dotenv
# import os

# load_dotenv()

# data = os.getenv("DATABASE_URL")
engine = create_engine("sqlite:///./test1.db",echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()