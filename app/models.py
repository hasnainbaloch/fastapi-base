from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# Local imports
from .database import Base


class TodoList(Base):
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key=True, nullable=False)
    todo = Column(String, nullable=False)
    complete = Column(Boolean, server_default='FALSE')
    deleted = Column(Boolean, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), nullable=False)
    sub_tasks = relationship("SubTodos")


class SubTodos(Base):
    __tablename__ = "sub_todos"

    id = Column(Integer, primary_key=True, nullable=False)
    label = Column(String, nullable=False)
    description = Column(String, nullable=False)
    complete = Column(Boolean, server_default='FALSE')
    deleted = Column(Boolean, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    todo_id = Column(Integer, ForeignKey(
        "todo_list.id", ondelete="CASCADE"), nullable=False)


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False, unique=True)
    last_name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
