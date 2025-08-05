from fastapi import FastAPI
from app.api.endpoints import router as book_router

# Инициализация API
app = FastAPI()

# Подключение роутера для работы с книгами
app.include_router(book_router, prefix="/books")
