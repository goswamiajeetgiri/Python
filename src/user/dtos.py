from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    fname: str
    lname: str
    email: str
    password: str
    createdBy: Optional[int] = None
    createdOn: Optional[datetime] = None
    modifiedBy: Optional[int] = None
    modifiedOn: Optional[datetime] = None
    isActive: bool = False


class UserResponseSchema(BaseModel):
    fname: str
    lname: str
    email: str
    id:int

class LoginSchema(BaseModel):
    username: str
    password: str
