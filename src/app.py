from fastapi import FastAPI
from src.database.database import Base,engine
from src.resource.user.api import user_router
from src.resource.task.api import task_router

Base.metadata.create_all(bind=engine)
app= FastAPI()

app.include_router(user_router)
app.include_router(task_router)

@app.get("/")
def read_root():
    return {"massage":"Hello Python!"}