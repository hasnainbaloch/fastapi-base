from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List


class SubTask(BaseModel):
    id: Optional[int]
    label: Optional[str]
    description: Optional[str] = ""
    complete: Optional[bool]
    deleted: Optional[bool]
    created_at: Optional[datetime]
    todo_id: Optional[int]

    class Config:
        orm_mode = True


class SubTaskResponse(BaseModel):
    id: Optional[int]
    label: Optional[str]
    description: Optional[str] = ""
    todo_id: int

    class Config:
        orm_mode = True


class ListItem(BaseModel):
    todo: str
    complete: Optional[bool] = False
    deleted: Optional[bool] = False


class ItemUpdate(BaseModel):
    id: int
    complete: Optional[bool] = False
    deleted: Optional[bool] = False


class TaskUpdate(BaseModel):
    complete: Optional[bool] = False
    deleted: Optional[bool] = False


class FilterType(BaseModel):
    type: str


class Users(BaseModel):
    email: EmailStr
    password: str


class NewUser(Users):
    first_name: str
    last_name: str
    # gender: typing.Literal['male', 'female']


class TokenData(BaseModel):
    id: Optional[str] = None


# schema/alter response that need to be sent to client
class Todo(ListItem):
    id: int
    created_at: datetime
    sub_tasks: Optional[List[SubTask]] = []

    class Config:
        orm_mode = True


# schema/alter response that need to be sent to client
class UsersResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):

    access_token: str
    token_type: str

    class Config:
        orm_mode = True
