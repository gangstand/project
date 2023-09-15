from typing import Optional
from pydantic import BaseModel


class Customer(BaseModel):
    name: Optional[str]
    iin: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Name",
                "iin": "1000000000",
            }
        }
