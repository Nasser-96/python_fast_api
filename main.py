from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the allowed origins
    allow_credentials=True,
)

class Category(Enum):
    PERSONAL = 'PERSONAL'
    WORK = 'WORK'

class Todo(BaseModel):
    title:str = Field(min_length=3)
    completed:bool
    id:int = Field(ge=3)
    category:Category

    @field_validator("id", mode="before")
    def check_id_before(cls, value: int):
        assert value, 'GGs' # here another validation before enter the above DTO
        return value
    
    @model_validator(mode="after")
    def check_title_after(self):
        assert self.title != "what", " 'what' is Not allowed" # here another validation after enter the above DTO
        return self


toDos = {
        0:Todo(title='first_title', category=Category.PERSONAL, completed=True,id=4),
        1:Todo(title='second_title', category=Category.WORK, completed=False,id=3),
    }


@app.get('/')
def index():
    return {'toDos':toDos}

@app.get('/todo/{todo_id}')
def get_todo_by_id(todo_id:int):
    if todo_id not in toDos:
        raise HTTPException(status_code=404, detail=f'ID {todo_id} does not exist')
    return toDos[todo_id]

@app.get('/todo')
def get_completed_toDos(Hello:str, gg:str,is_completed:Optional[bool]=None) -> dict[str, list[Todo]]:
    if is_completed:
        filtered_toDos = [todo for todo in toDos.values() if todo.completed is is_completed ]
        return {'toDos':filtered_toDos}
    print("HELLLOOOO")
    return {'toDos':[]}

@app.post('/')
def create_todo(todo:Todo) -> dict:
    if not '':
        print("HERE")
    if todo.id in toDos:
        raise HTTPException(status_code=400, detail=f'ID {todo.id} already exist')
    toDos[todo.id] = todo
    return {'new_toDos': toDos}