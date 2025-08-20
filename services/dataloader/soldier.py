from pydantic import BaseModel

class Soldier(BaseModel):
    ID: int
    first_name: str
    last_name: str
    phone_number: str
    rank: str
