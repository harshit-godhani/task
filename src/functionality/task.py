from fastapi import Depends,Security,HTTPException
from src.database.database import get_db
from sqlalchemy.orm import Session
from src.resource.task.model import TaskModel
from src.resource.task.schema import TaskCreateSchema,TaskUpdateSchema
from src.utils.utils import verify_token
from fastapi.security import HTTPBearer
from src.resource.user.model import UserModel

security = HTTPBearer()

def create_task(task: TaskCreateSchema, db: Session = Depends(get_db), token: str = Security(security)):
    user = verify_token(token.credentials)

    if not user["id"]:
        raise HTTPException(status_code=400,detail="user not found")

    task_data = TaskModel(
        title=task.title,
        description=task.description,
        status=task.status,
        owner_id = user["id"] 

    )

    db.add(task_data)
    db.commit()
    db.refresh(task_data)

    return {
        "success": True,
        "message": "Task created successfully",
        "user_id":user["id"]
    }

def get_task(onwer_id:int,db:Session=Depends(get_db)):
    data = db.query(TaskModel).filter(TaskModel.owner_id == onwer_id).first()

    if not data:
        raise HTTPException(status_code=400,detail="Task not found!!")
    return{
        "success":True,
        "massage":"This is your task.",
        "task_id":data.id
    }

def update_task(task:TaskUpdateSchema,db:Session=Depends(get_db)):

    data1 = db.query(TaskModel).filter(TaskModel.id == task.id).first()
    if not data1:
        raise HTTPException(status_code=400,detail="Task not found!!")
    
    data1.title=task.title,
    data1.description=task.description,
    data1.status=task.status,
    data1.owner_id=task.owner_id

    db.commit()
    return{
        "success":True,
        "massage":"Your task update successfully.",
        "task_id":task.id
    }

def delete_task(task_id:int,db:Session=Depends(get_db)):
    db_data = db.query(TaskModel).filter(TaskModel.id == task_id.id).first()

    if not db_data:
        raise HTTPException(status_code=400,detail="task not found!!")
    
    db.delete(db_data)
    db.commit()

    return{
        "success":True,
        "massage":"Task delte successfully",
        "task_id":task_id
    }