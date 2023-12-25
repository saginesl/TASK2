from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    email: str


class Task(BaseModel):
    id: int
    id_user: int
    title: str
    content: str