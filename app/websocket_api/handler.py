# Обработка сообщений от клиента
from app.core.storage import book_storage, BookModel


async def handle_message(message):
    if message == "ping":
        return "pong"
    if '/add_book' in message:
        args = message.split(' ')
        if len(args) == 2:
            try:
                book = BookModel(title=args[1])
                await book_storage.add_book(book)
                return f'Книга "{book.title}" c ID {book.id} добавлена!'
            except Exception as e:
                return f'Ошибка: {e}'
    return 'К сожалению мой функционал ограничен :('
