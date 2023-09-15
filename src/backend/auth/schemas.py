from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@flagman-it.ru",
                "password": "password",
            }
        }


class UserLogin(BaseModel):
    email: Optional[str]
    password: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@flagman-it.ru",
                "password": "password",
            }
        }


class UserUpdate(BaseModel):
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "last_name": "last_name",
                "first_name": "first_name",
                "middle_name": "middle_name",
            }
        }
