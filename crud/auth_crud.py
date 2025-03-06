import random
import string
from db.database import *
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends,Header,Request,status,HTTPException
from typing import Optional, Union


async def generate_token(db: Session,payload):
    db_object = db.query(User).filter(User.email == payload.email).first()
    
    if db_object:
        for key in db_object.api_keys:
            key.is_valid = False
            db.add(key)
        token = ''.join(random.choice(string.ascii_uppercase +
                            string.digits + string.ascii_lowercase) for _ in range(64))
        db_item = APIKeys(token=token, is_valid=True, user_id=db_object.id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        return {"Error": "No user found"}
