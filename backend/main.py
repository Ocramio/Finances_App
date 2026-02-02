from typing import Annotated
from fastapi import FastAPI,  Depends, HTTPException
from dependencies import db_dependency
from starlette import status
import pandas as pd
from routers import auth
from sqlalchemy import select, text

app = FastAPI()

app.include_router(auth.router)

user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@app.get("/finances/add",status_code=status.HTTP_200_OK)
async def add_expense(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    test = db.execute(text("SELECT * FROM public.finances_app_users")).mappings().all()
    print(test)
    return test