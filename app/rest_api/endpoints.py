from fastapi import APIRouter, HTTPException, Query

from app.rest_api.schemas import (
    BookResponse,
    BookCreate,
    BookUpdate,
    BookFilter,
)
from app.core.storage import book_storage, BookModel
from app.websocket_api.manager import manager


# Инициализация роутера, отвечающего за работу с книгами
router = APIRouter()


# 1. Получение списка всех книг
@router.get('/')
@manager.notify(
    "[INFO] REST: Получение списка всех книг",
    "book_updates"
    )  # См. Websocket API
@manager.notify(
    """[INFO] REST: Получение списка всех книг:
        function: {func_name},
        title: {title},
        id__lt: {id__lt},
        id__gt: {id__gt},
        return: {result},
        error: {error}
    """,
    "admin_notifications"
    )  # См. Websocket API
async def get_books(
    title: str | None = Query(None, max_length=100),
    id__lt: int | None = Query(None),
    id__gt: int | None = Query(None)
        ) -> dict[str, list[BookResponse]]:
    filters = BookFilter(
        title=title,
        id__lt=id__lt,
        id__gt=id__gt,
    )
    books = await book_storage.get_books(**filters.model_dump())
    return {"books": [BookResponse(**(await book.json)) for book in books]}


# 2. Добавление новой книги
@router.post('/')
@manager.notify(
    "[INFO] REST: Добавление новой книги",
    "book_updates"
    )  # См. Websocket API
@manager.notify(
    """[INFO] REST: Добавление новой книги:
        function: {func_name},
        book: {book},
        return: {result},
        error: {error}
    """,
    "admin_notifications"
    )  # См. Websocket API
async def add_book(book: BookCreate) -> dict[str, BookResponse]:
    book_to_add = BookModel(**book.model_dump())
    await book_storage.add_book(book_to_add)
    return {"book": BookResponse(**(await book_to_add.json))}


# 3. Получение конкретной книги
@router.get('/{book_id}')
@manager.notify(
    "[INFO] REST: Получение конкретной книги",
    "book_updates"
    )  # См. Websocket API
@manager.notify(
    """[INFO] REST: Получение конкретной книги:
        function: {func_name},
        book_id: {book_id},
        return: {result},
        error: {error}
    """,
    "admin_notifications"
    )  # См. Websocket API
async def get_book(book_id: int) -> dict[str, BookResponse | None]:
    book = await book_storage.get_book(book_id)
    if book:
        return {"book": BookResponse(**(await book.json))}
    raise HTTPException(status_code=404, detail="Book not found")


# 4. Удаление книги
@router.delete('/{book_id}')
@manager.notify(
    "[INFO] REST: Удаление книги",
    "book_updates"
    )  # См. Websocket API
@manager.notify(
    """[INFO] REST: Удаление книги:
        function: {func_name},
        book_id: {book_id},
        return: {result},
        error: {error}
    """,
    "admin_notifications"
    )  # См. Websocket API
async def delete_book(book_id: int) -> dict[str, bool]:
    success = await book_storage.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {'success': success}


# 5. Обновление книги
@router.put('/{book_id}')
@manager.notify(
    "[INFO] REST: Получение списка всех книг",
    "book_updates"
    )  # См. Websocket API
@manager.notify(
    """[INFO] REST: Обновление книги:
        function: {func_name},
        book: {book},
        book_id: {book_id},
        return: {result},
        error: {error}
    """,
    "admin_notifications"
    )  # См. Websocket API
async def update_book(
    book_id: int,
    book: BookUpdate
        ) -> dict[str, BookResponse | None]:
    updated_book = await book_storage.update_book(book_id, **book.model_dump())
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": BookResponse(**(await updated_book.json))}
