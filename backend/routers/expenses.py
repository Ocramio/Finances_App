from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from dependencies import db_dependency
from starlette import status
import pandas as pd
from routers import auth
from sqlalchemy import insert, select, text
from models import Expense

class ExpenseResponse(BaseModel):
    expense_id: int
    expense_type: str
    expense_value: float
    expense_description: str

class CreateExpenseModel(BaseModel):
    expense_type: str
    expense_value: float
    expense_description: str

router = APIRouter(
    prefix='/expenses',
    tags=['expenses']
)

user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@router.get("/list",status_code=status.HTTP_200_OK, response_model=list[ExpenseResponse])
async def list_expenses(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    user_expenses_list = db.query(Expense)
    return user_expenses_list

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_expense(db: db_dependency, user: user_dependency, expense_model: list[CreateExpenseModel]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    expenses_to_add = []
    for expense in expense_model:
        expenses_to_add.append({
            'expense_type': expense.expense_type,
            'expense_value': expense.expense_value,
            'expense_description': expense.expense_description,
            'user_id': user.get('user_id')
        })

    db.execute(insert(Expense), expenses_to_add)
    db.commit()

    return f"{len(expenses_to_add)} expenses inserted"
   
@router.put("/update")
async def create_expense(db: db_dependency, user: user_dependency, expense_model: list[CreateExpenseModel]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

@router.delete("/delete")
async def create_expense(db: db_dependency, user: user_dependency, expense_model: list[CreateExpenseModel]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    