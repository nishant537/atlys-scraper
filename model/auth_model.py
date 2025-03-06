from pydantic import BaseModel
from typing import Optional, List

class GenerateTokenSchema(BaseModel):
    email: str
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "user@test.com"
            }
        }