
from pydantic import BaseModel


# Схема для ответа
class BookResponse(BaseModel):
    id: int
    title: str


# Схема для создания
class BookCreate(BaseModel):
    title: str


# Схема для обновления
class BookUpdate(BaseModel):
    title: str
