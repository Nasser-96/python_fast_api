from fastapi import Depends
from app.common_deps import get_db_session_dependency
from app.common.db import db

get_db_session = get_db_session_dependency(db.SessionLocal)
db_session = Depends(get_db_session)