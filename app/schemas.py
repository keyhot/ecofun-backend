from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from .responses import Bin
from fastapi import UploadFile

class VerifyPhoto(BaseModel):
    user_id: str = Field(..., example="example@gmail.com")
    binTypeGuess: Bin

class User(BaseModel):
    id: str
    score: int

    class Config:
        from_attributes = True


class CreateUser(User):
    class Config:
        from_attributes = True