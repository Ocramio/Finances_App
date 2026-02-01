from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dependencies import get_session
from typing import Annotated, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import insert
from models import User
from dependencies import db_dependency

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserBasemodel(BaseModel) :
    email: str
    first_name: str
    last_name: str
    password: str

#def authenticate_user(user, password, db: db_dependency):
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user_model: List[CreateUserBasemodel]):

    # Transforma cada item em dict e já faz hash da senha
    users_to_insert = []
    for u in user_model:
        users_to_insert.append({
            "user_email": u.email,
            "user_first_name": u.first_name,
            "user_last_name": u.last_name,
            "user_hashed_password": bcrypt_context.hash(u.password)
        })

    db.execute(insert(User), users_to_insert)
    db.commit()

    return {"inserted": len(user_model)}

