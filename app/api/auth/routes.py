from fastapi import APIRouter
from sqlalchemy.orm.session import Session
from ...dependencies import db_session
from app.api.auth.services.auth import get_all_users_,signup_,logIn_
from app.api.schemas import AuthRequest

router = APIRouter(prefix='/auth')

@router.get('/users')
def get_all_users(session: Session = db_session):
    return get_all_users_(session=session)

@router.post('/signup')
def signup(user_data:AuthRequest,session: Session = db_session):
    return signup_(session=session,user_data=user_data)

@router.post('/login')
def logIn(user:AuthRequest,session: Session = db_session):
    return logIn_(session=session,user=user)