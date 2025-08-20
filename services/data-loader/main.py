from fastapi import FastAPI
from crud import CRUD
from soldier import Soldier

app = FastAPI()
crud = CRUD()


@app.post("/insert")
def insert_data(soldier: Soldier):
    return crud.create(soldier)



