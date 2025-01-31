from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config import Config

DATABASE_URl = Config.DB_URL

engine = create_engine(DATABASE_URl,echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()