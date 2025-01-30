from pydantic import BaseModel

class TaskCreateSchema(BaseModel):
    title : str
    description : str
    status : str

class TaskUpdateSchema(BaseModel):
    id : int
    title : str
    description : str
    status : str