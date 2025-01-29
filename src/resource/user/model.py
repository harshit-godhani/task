from sqlalchemy import Column, Integer, String
from src.database.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,nullable=False,unique=True)
    email =Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(String,nullable=False)