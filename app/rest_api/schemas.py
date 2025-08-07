
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


# Схема фильтров
class BookFilter(BaseModel):
    title: str | None = None
    id: int | None = None
    id__lt: int | None = None
    id__gt: int | None = None
