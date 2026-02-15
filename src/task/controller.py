from src.task.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.task.models import TaskModel
from fastapi import HTTPException


def create_task(body:TaskSchema, db:Session):
    data=body.model_dump()
    new_task=TaskModel(title=data["title"],description=data["description"],is_completed=data["is_completed"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status":"Task created", "data":new_task}

def get_task(db:Session):
    task=db.query(TaskModel).all()
    return {"status":'Get data',"data":task}

def get_task_by_id(id:int,db:Session):
    one_task=db.query(TaskModel).get(id)
    if not one_task:
        return HTTPException(404,"Not found")
    return {"status":'Get data',"data":one_task}