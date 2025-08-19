from typing import Optional

from pydantic import BaseModel

class Soldier(BaseModel):
    ID: Optional[int] = None
    first_name: str
    last_name: str
    phone_number: str
    rank: str
