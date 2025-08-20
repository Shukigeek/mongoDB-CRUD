from fastapi import FastAPI
from crud import CRUD
from soldier import Soldier

app = FastAPI()
crud = CRUD()


@app.post("/insert")
def insert_data(soldier: Soldier):
    return crud.create(soldier)


@app.get("/read")
def get_data(ID: int = None, first_name: str = None):
    return crud.read(ID=ID, first_name=first_name)


@app.put("/update/{ID}")
def update_data(ID: int, updates: dict):
    return crud.update(ID, updates)



