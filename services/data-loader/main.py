from fastapi import FastAPI
from soldier import Soldier
from crud import CRUD
import uvicorn

app = FastAPI()
crud = CRUD()

# GET all soldiers in db
@app.get("/soldiersdb/")
def get_all_soldiers():
    return crud.read()

# GET one selected soldier in db
@app.get("/soldiersdb/{soldier_id}")
def get_soldier(soldier_id: int):
    return crud.read(ID=soldier_id)

# POST insert new soldier/s
@app.post("/soldiersdb/")
def create_soldier(soldier: Soldier):
    return crud.create(soldier)

# PUT update soldier by id
@app.put("/soldiersdb/{soldier_id}")
def update_soldier(soldier_id: int, updates: dict):
    return crud.update(soldier_id, updates)

# DELETE soldier by id
@app.delete("/soldiersdb/{soldier_id}")
def delete_soldier(soldier_id: int):
    return crud.delete(soldier_id)


if __name__ == '__main__':
    uvicorn.run(app,host="localhost",port=8000)