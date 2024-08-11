from fastapi import FastAPI, HTTPException
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


todos = {
    0:Todo(title='first_title', category=Category.PERSONAL, completed=True,id="12"),
    1:Todo(title='second_title', category=Category.WORK, completed=False,id=2),
}

@app.get('/')
def index():
    return {'todos':todos}

@app.get('/todo/{todo_id}')
def get_todo_by_id(todo_id:int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail=f'ID {todo_id} does not exist')
    return todos[todo_id]