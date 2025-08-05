from fastapi import APIRouter, HTTPException

from app.api.schemas import BookResponse, BookCreate, BookUpdate
from app.core.storage import book_storage, BookModel


# Инициализация роутера, отвечающего за работу с книгами
router = APIRouter()


# 1. Получение списка всех книг
@router.get('/')
async def get_books() -> dict[str, list[BookResponse]]:
    books = book_storage.get_books()
    return {"books": [BookResponse(**book.json) for book in books]}


# 2. Добавление новой книги
@router.post('/')
async def add_book(book: BookCreate) -> dict[str, BookResponse]:
    book_to_add = BookModel(**book.model_dump())
    book_storage.add_book(book_to_add)
    return {"book": BookResponse(**book_to_add.json)}


# 3. Получение конкретной книги
@router.get('/{book_id}')
async def get_book(book_id: int) -> dict[str, BookResponse | None]:
    book = book_storage.get_book(book_id)
    if book:
        return {"book": BookResponse(**book.json)}
    raise HTTPException(status_code=404, detail="Book not found")


# 4. Обновление книги
@router.delete('/{book_id}')
async def delete_book(book_id: int) -> dict[str, bool]:
    success = book_storage.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {'success': success}


# 5. Удаление книги
@router.put('/{book_id}')
async def update_book(
    book_id: int,
    book: BookUpdate
        ) -> dict[str, BookResponse | None]:
    updated_book = book_storage.update_book(book_id, **book.model_dump())
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": BookResponse(**updated_book.json)}
