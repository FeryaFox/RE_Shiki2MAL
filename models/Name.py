from pydantic import BaseModel


class Name(BaseModel):
    name: str
    language: str
