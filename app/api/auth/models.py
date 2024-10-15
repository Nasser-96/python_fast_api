from sqlalchemy import Column, Integer, String
from app.common.db import Base

class UserData(Base):
    __tablename__ = "user_data"  # Table name

    id = Column(Integer, primary_key=True, autoincrement=True)  # id field with auto-increment
    username = Column(String, unique=True, nullable=False)  # unique username
    password = Column(String, nullable=False)