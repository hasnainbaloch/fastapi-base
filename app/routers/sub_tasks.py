from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Union
from sqlalchemy.orm import Session

# local imports
from app.schemas import ListItem, FilterType, ItemUpdate, Todo, SubTask, SubTaskResponse, TaskUpdate
from app import models, oAuth2
from app.models import SubTodos, TodoList
from app.database import get_db

router = APIRouter(
    prefix='/task',
    tags=["Sub Tasks"]
)


# Subtask routes
@router.post("", status_code=status.HTTP_201_CREATED,  response_model=SubTaskResponse)
async def create_list_item(new_item: SubTaskResponse, db: Session = Depends(get_db)):

    # ORM query (SqlAlchemy)
    task = SubTodos(**new_item.dict())

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{index_id}", status_code=status.HTTP_201_CREATED)
async def update_item(index_id: int, update: TaskUpdate, db: Session = Depends(get_db)):

    # ORM query (SqlAlchemy)
    post_query = db.query(SubTodos).filter(SubTodos.id == index_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(update.dict(), synchronize_session=False)
    db.commit()


@router.delete("/{index_id}", status_code=status.HTTP_201_CREATED)
async def update_item(index_id: int, db: Session = Depends(get_db)):

    # ORM query (SqlAlchemy)
    post_query = db.query(SubTodos).filter(SubTodos.id == index_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.delete(synchronize_session=False)
    db.commit()
