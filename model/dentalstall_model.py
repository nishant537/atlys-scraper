from typing import List

from pydantic import BaseModel

def Product(BaseModel):
    name: str
    price: float
    image: str