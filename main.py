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
    id:int
    category:Category

    @field_validator("id", mode="before")
    def check_id_before(cls, value: int):
        assert len(str(value)) >= 1, 'id length most be 1 or greater' # here another validation before enter the above DTO
        return value
    
    @model_validator(mode="after")
    def check_title_after(self):
        assert self.title != "what", " 'what' is Not allowed" # here another validation after enter the above DTO
        return self


toDos = {
        0:Todo(title='first_title', category=Category.PERSONAL, completed=True,id=0),
        1:Todo(title='second_title', category=Category.WORK, completed=False,id=1),
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
def get_completed_toDos(Hello:str, gg:str,is_completed:Optional[bool]=None) -> dict[str, list[Todo]]: # here (gg and Hello) are query params
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

@app.put('/todo/{todo_id}')
def update_todo(todo_id:int,todo:Todo):
    if todo_id not in toDos:
        raise HTTPException(status_code=400,detail=f'ID {todo_id} not exist so we can not update it')
    toDos[todo_id] = todo
    print(type(todo))
    return {'new_toDos': toDos}