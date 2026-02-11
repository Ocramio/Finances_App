from typing import Annotated
from fastapi import FastAPI,  Depends, HTTPException
from dependencies import db_dependency
from starlette import status
import pandas as pd
from routers import auth, expenses
from sqlalchemy import select, text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# app.mount(
#     "/",
#     StaticFiles(directory=os.path.join(BASE_DIR, "..", "frontend"), html=True),
#     name="frontend"
# )
