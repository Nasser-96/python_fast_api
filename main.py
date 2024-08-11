from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Category(Enum):
    PERSONAL = 'PERSONAL'
    WORK = 'WORK'

class Todo(BaseModel):
    title:str
    completed:bool
    id:int
    category:Category


ggs = Todo(title='first_title', category=Category.PERSONAL, completed=False,id="12")

print(ggs.title)