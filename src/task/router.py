from fastapi import APIRouter,Depends
from src.task import controller
from src.task.dtos import TaskSchema
from src.utils.db import get_db


task_routes=APIRouter(prefix="/task")


@task_routes.post("/create")
def create_task(body:TaskSchema, db=Depends(get_db)):
    return controller.create_task(body,db)

@task_routes.get("/get_all_task")
def get_all_task(db=Depends(get_db)):
    return controller.get_task(db)

@task_routes.get("/get_task_by_id/{id}")
def get_task_by_id(id:int,db=Depends(get_db)):
    return controller.get_task_by_id(id,db)


