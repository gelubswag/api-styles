# Хранилище с книгами (таблица)
# По-хорошему, следует использовать БД
# Но для примера подойдёт и работа со списком

# Модель книги в "БД"
import asyncio


class BookModel:
    def __init__(self, title: str, id: int = 0):
        self.id: int = id
        self.title: str = title

    def __str__(self):
        return f"Book(id={self.id} title={self.title})"

    def __repr__(self):
        return f"Book(id={self.id} title={self.title})"

    @property
    async def json(self):
        return {str(key): value for key, value in self.__dict__.items()}


# Таблица с книгами
class BookStorage:

    def __init__(self):
        self.books: list[BookModel] = []
        self.index: int = 0
        self.allowed_filters = {
            "id__gt": lambda book, value: book.id > value,
            "id__lt": lambda book, value: book.id < value,
            "id": lambda book, value: book.id == value,
            "title": lambda book, value: book.title == value,
        }
        self.lock = asyncio.Lock()

    def where(
        self,
        book,
        **filters
            ) -> bool:
        for key, func in self.allowed_filters.items():
            if key not in filters:
                continue
            value = filters.get(key)
            if not value:
                continue
            if not func(book, value):
                return False
        return True

    async def add_book(self, book: BookModel) -> None:
        async with self.lock:
            book.id = self.index
            self.index += 1
            self.books.append(book)

    async def get_books(
        self,
        id: int | None = None,
        title: str | None = None,
        id__gt: int | None = None,
        id__lt: int | None = None,
            ) -> list[BookModel]:
        async with self.lock:
            return [
                book
                for book in self.books
                if self.where(
                    book=book,
                    id=id,
                    title=title,
                    id__gt=id__gt,
                    id__lt=id__lt,
                    )
            ]

    async def get_book(
        self,
        id: int | None = None,
        title: str | None = None
            ) -> BookModel | None:
        async with self.lock:
            if id is not None:
                for book in self.books:
                    if book.id == id:
                        return book
                return None
            if title is not None:
                for book in self.books:
                    if book.title == title:
                        return book
                return None

    async def delete_book(self, book_id: int) -> bool:
        async with self.lock:
            for book in self.books:
                if book.id == book_id:
                    self.books.remove(book)
                    return True
        return False

    async def update_book(self, book_id: int, title: str) -> BookModel | None:
        async with self.lock:
            for book in self.books:
                if book.id == book_id:
                    book.title = title
                    return book
            return None


book_storage = BookStorage()
