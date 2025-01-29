from sqlalchemy import *
from src.database.database import Base
from sqlalchemy.orm import Relationship

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    status = Column(String,nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="cascade"))
    user = Relationship("UserModel")
