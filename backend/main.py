from typing import Annotated
from fastapi import FastAPI,  Depends
from routers import auth, expenses
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.include_router(auth.router)
app.include_router(expenses.router)

user_dependency = Annotated[dict, Depends(auth.get_current_user)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

