from typing import Annotated, Optional
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from dependencies import db_dependency
from starlette import status
from routers import auth
from sqlalchemy import insert
from models import Income
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix='/incomes',
    tags=['incomes']
)

class IncomeResponse(BaseModel):
    income_id: int
    income_type: str
    income_value: float
    income_description: str

class CreateIncomeModel(BaseModel):
    income_type: str
    income_value: float
    income_description: str

class UpdateIncomeModel(BaseModel):
    income_type: Optional[str] = None
    income_value: Optional[float] = None
    income_description: Optional[str] = None

user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@router.get("/list",status_code=status.HTTP_200_OK, response_model=list[IncomeResponse])
async def list_income(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    user_incomes_list = db.query(Income).filter(user.get("user_id") == Income.user_id)
    return user_incomes_list

@router.get("/{income_id}",status_code=status.HTTP_200_OK, response_model=IncomeResponse)
async def select_income(income_id: int, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    user_income = db.query(Income).filter((user.get("user_id") == Income.user_id), (income_id == Income.income_id)).first()
    return user_income

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_income(db: db_dependency, user: user_dependency, income_model: list[CreateIncomeModel]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    incomes_to_add = []
    for income in income_model:
        incomes_to_add.append({
            'Income_type': income.Income_type,
            'Income_value': income.Income_value,
            'Income_description': income.Income_description,
            'user_id': user.get('user_id')
        })

    db.execute(insert(Income), incomes_to_add)
    db.commit()

    return f"{len(incomes_to_add)} Incomes inserted"
   
@router.put("/update/{income_id}", status_code= status.HTTP_200_OK)
async def update_income(db: db_dependency, user: user_dependency, income_id: int, update_model: UpdateIncomeModel):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    income = db.query(Income).filter(Income.income_id == income_id).first()
    
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Income of id: {income_id} not found")

    update_data = update_model.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(income, key, value)

    db.commit()
    db.refresh(income)

    return income
    
@router.delete("/delete/{income_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_income(db: db_dependency, user: user_dependency, income_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    income = db.query(Income).filter(Income.income_id == income_id).first()
    
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Income of id: {income_id} not found")

    db.delete(income)

    db.commit()

    return None