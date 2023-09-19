from typing import Optional
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import Column, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    gender = Column(String)
    role = Column(String)


class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"

class User(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Gender
    role: Role

class UserUpdateRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    role: Optional[Role]

