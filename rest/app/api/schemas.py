# Схемы для API запросов
from pydantic import BaseModel


class BookResponse(BaseModel):
    id: int
    title: str


class BookCreate(BaseModel):
    title: str


class BookUpdate(BaseModel):
    title: str
