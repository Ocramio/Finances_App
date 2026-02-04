from typing import Annotated
from fastapi import FastAPI,  Depends, HTTPException
from dependencies import db_dependency
from starlette import status
import pandas as pd
from routers import auth, expenses
from sqlalchemy import select, text

app = FastAPI()

app.include_router(auth.router)
app.include_router(expenses.router)

user_dependency = Annotated[dict, Depends(auth.get_current_user)]