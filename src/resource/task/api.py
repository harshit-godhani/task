from fastapi import Depends,HTTPException,APIRouter, Security
from sqlalchemy.orm import Session
from src.resource.task.schema import TaskCreateSchema,TaskUpdateSchema
from src.functionality.task import create_task,update_task,delete_task,get_task
from src.database.database import get_db
from fastapi.security import HTTPBearer

security = HTTPBearer()

task_router = APIRouter(tags=["CRUD task"])

@task_router.post("/create/task/")
def reg_task(task:TaskCreateSchema,db:Session= Depends(get_db),token:str=Security(security)):
    try:
        task = create_task(task=task,db=db,token=token)
        return task
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    
@task_router.patch("/update/task/")
def log_task(task:TaskUpdateSchema,db:Session= Depends(get_db), token: str = Security(security)):
    try:
        task = update_task(task=task,db=db,token=token)
        return task

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    
@task_router.get("/get/task/")
def task_get_by_id(onwer_id:int,db:Session=Depends(get_db)):
    try:
        task = get_task(onwer_id=onwer_id,db=db)
        return task
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

@task_router.delete("/delete/task/")
def del_task(task_id:int,db:Session=Depends(get_db)):
    try:
        task = delete_task(task_id=task_id,db=db)
        return task
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    

