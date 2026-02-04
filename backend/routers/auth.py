from datetime import timedelta, datetime, timezone
import os
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated, List
from pydantic import BaseModel
from sqlalchemy import insert
from models import User
from dependencies import db_dependency
from jose import JWTError, jwt
from dotenv import load_dotenv
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserBasemodel(BaseModel) :
    email: str
    first_name: str
    last_name: str
    password: str
    role: str = "user"

class AccessToken(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(user_email, password, db: db_dependency):
    # Valida o usuário
    user = db.query(User).filter(User.user_email == user_email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.user_hashed_password):
        return False
    return user

def create_access_token(user_email:str, user_id: int, expires_delta: timedelta):
    encode = {'sub': user_email, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user_email: str = payload.get('sub')
        user_id: str = payload.get('id')
        if user_email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        return {'user_email': user_email, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_model: CreateUserBasemodel):

    # Transforma cada item em dict e já faz hash da senha
    user_to_insert = {
        "user_email": user_model.email,
        "user_first_name": user_model.first_name,
        "user_last_name": user_model.last_name,
        "user_hashed_password": bcrypt_context.hash(user_model.password),
        "user_role": str.upper(user_model.role).strip()
    }

    if(user_to_insert["user_role"] not in ["USER", "ADMIN"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User role not available")

    db.execute(insert(User), user_to_insert)
    db.commit()

    return "User created successfully"

@router.post("/token", status_code=status.HTTP_200_OK, response_model=AccessToken)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
    token = create_access_token(user.user_email, user.user_id, expires_delta=timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

