from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local imports
from app.routers import todo, user, auth, sub_tasks
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8081",
    "http://localhost:3000",
    "http://localhost:4173",
    "http://192.168.1.5:4173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
# app.include_router(user.router)
app.include_router(todo.router)
app.include_router(sub_tasks.router)
