from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Union
from sqlalchemy.orm import Session

# local imports
from app.schemas import ListItem, FilterType, ItemUpdate, Todo, SubTask, SubTaskResponse
from app import models, oAuth2
from app.models import SubTodos, TodoList
from app.database import get_db

router = APIRouter(
    prefix='/list',
    tags=["Todos"]
)


@router.get("", response_model=List[Todo])
async def get_list(db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # Raw SQL query
    # cursor.execute("""SELECT * FROM todo_list""")
    # todo_list = cursor.fetchall()
    # ORM query (SqlAlchemy)
    todo_list = db.query(TodoList).join(SubTodos, full=True).filter(TodoList.owner_id == current_user.id).all()
    return todo_list


@router.post("", response_model=Todo)
async def create_list_item(new_item: ListItem, db: Session = Depends(get_db),
                           current_user: int = Depends(oAuth2.get_current_user)):
    # Raw SQL Query
    # cursor.execute("""INSERT INTO todo_list (todo, complete, deleted) VALUES (%s, %s, %s) RETURNING * """,
    #                (new_item.todo, new_item.complete, new_item.deleted))
    # new_todo = cursor.fetchone()
    # conn.commit()

    # ORM query (SqlAlchemy)
    new_todo = TodoList(owner_id=current_user.id, **new_item.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.delete("/{index_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(index_id: int, db: Session = Depends(get_db)):
    # Raw SQL query
    # cursor.execute(""" DELETE FROM todo_list WHERE id = %s RETURNING *""", (str(index_id),))
    # conn.commit()

    # ORM query (SqlAlchemy)
    post = db.query(TodoList).filter(TodoList.id == index_id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {index_id} is not valid or does not exist")

    post.delete(synchronize_session=False)
    db.commit()


@router.patch("", status_code=status.HTTP_201_CREATED, )
async def update_item(update: ItemUpdate, db: Session = Depends(get_db),
                      current_user: int = Depends(oAuth2.get_current_user)):
    # Raw SQL query
    # cursor.execute(f"""UPDATE todo_list SET {update.type} = %s WHERE id = %s RETURNING *""",
    #                (update.done, str(index_id),))
    # cursor.fetchone()
    # conn.commit()

    # ORM query (SqlAlchemy)
    post_query = db.query(TodoList).filter(TodoList.id == update.id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(update.dict(), synchronize_session=False)
    db.commit()
