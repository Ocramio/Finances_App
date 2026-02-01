from fastapi import FastAPI,  Depends, HTTPException
from dependencies import db_dependency
from starlette import status
import pandas as pd
from routers import auth
from sqlalchemy import select, text

app = FastAPI()

app.include_router(auth.router)

@app.get("/finances/add",status_code=status.HTTP_200_OK)
async def add_expense(db: db_dependency):
    test = db.execute(text("SELECT * FROM public.finances_app_users")).mappings().all()
    print(test)
    return test