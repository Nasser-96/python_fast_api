import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select
from app.api.auth.models import UserData
from app.api.schemas import AuthRequest
import bcrypt
from app.helper import ReturnResponse
from jwt import PyJWTError

import jwt
from jwt import PyJWTError

load_dotenv()

def get_all_users_(session: Session):
    return session.query(UserData).all()

def signup_(session: Session,user_data:AuthRequest):
    foundUser: UserData | None = select_user_by_username(username=user_data.username,session=session)
    if foundUser:
        raise  HTTPException(status_code=400,detail=f'Username Already Exist')
    
    hashed_password = hash_password(user_data.password)
    user_data.password = hashed_password
    try:
        new_user = UserData(**user_data.model_dump())

        session.add(new_user)

        token = generate_token_(new_user)

        response_data = {
            "username": new_user.username,
        }

        return ReturnResponse(response={"token":token,"user_data":response_data},is_successful=True)
    except Exception as e:
        session.rollback()  # Rollback the transaction in case of error
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def logIn_(user:AuthRequest,session: Session):
    foundUser: UserData | None = select_user_by_username(username=user.username,session=session)
    isValidPassword =  bcrypt.checkpw(user.password.encode('utf-8'),foundUser.password.encode('utf-8'))

    if not foundUser or not isValidPassword:
         raise HTTPException(status_code=400,detail=f'username or password incorrect')
    
    token = generate_token_(foundUser)
    return ReturnResponse(response={"token":token},is_successful=True)

def generate_token_(user_data:UserData):
    secret_key = os.getenv("JSON_TOKEN_KEY")
    payload={'id':user_data.id,"username":user_data.username}

    try:
        # Generate the JWT
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token
    except PyJWTError as e:
        raise ValueError(f"JWT generation error: {str(e)}")
    
def select_user_by_username(username:str,session:Session):
    stmt = select(UserData).where(UserData.username == username)
    foundUser: UserData | None = session.execute(stmt).scalar_one_or_none()
    return foundUser