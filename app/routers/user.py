from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

# local imports
from app.schemas import Users, NewUser, UsersResponse
from .. import models, utils
from ..database import get_db


router = APIRouter(
    prefix='',
    tags=["Users"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UsersResponse)
async def create_user(new_user: NewUser, db: Session = Depends(get_db)):
    secure_password = utils.hash_password(new_user.password)
    new_user.password = secure_password

    # ORM query (SqlAlchemy)
    created_user = models.Users(**new_user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user


# @router.get("/{user_id}", response_model=UsersResponse)
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == user_id).first()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"user with id: {user_id} does not exist")
#     return user
