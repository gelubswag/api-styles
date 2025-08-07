import strawberry

from app.core.storage import BookModel, book_storage
from app.websocket_api.manager import manager


@strawberry.type(  # (декоратор, объявляющий тип ввода)
    description="""Книга
    - id: strawberry.ID | None - Идентификатор книги
    - title: str | None - Название книги"""
    )
class BookType:
    id: strawberry.ID | None
    title: str | None

    @classmethod
    def from_model(cls, model: BookModel):
        return cls(id=strawberry.ID(str(model.id)), title=model.title)


@strawberry.input(  # (декоратор, объявляющий тип ввода)
    description="""Данные для создания книги
    - title: str - Название книги"""
    )
class BookCreateInput:
    title: str


@strawberry.input(
    description="""Данные для обновления книги
    - title: str - Название книги"""
)
class BookUpdateInput:
    title: str


@strawberry.type  # (декоратор, объявляющий тип)
class Query:
    @strawberry.field(  # (декоратор, объявляющий поле)
        description="""Получить книги по фильтрам:
        - id: strawberry.ID | None - Идентификатор книги
        - title: str | None - Название книги
        - idGt: int | None - Идентификатор больше указанного
        """
        )
    @manager.notify(
        "[INFO] GraphQL: Получение книг по фильтрам",
        "book_updates"
        )  # См. Websocket API
    @manager.notify(
        """[INFO] GraphQL: Получение списка всех книг:
            function: {func_name},
            id: {id},
            title: {title},
            idLt: {id_lt},
            idGt: {id_gt},
            return: {result},
            error: {error}
        """,
        "admin_notifications"
        )  # См. Websocket API
    async def books(
        self,
        id: strawberry.ID | None = None,
        title: str | None = None,
        id_gt: int | None = None,
        id_lt: int | None = None
            ) -> list[BookType]:
        filters = {
            "id": id,
            "title": title,
            "id__gt": id_gt,
            "id__lt": id_lt
        }
        return [
            BookType(id=book.id, title=book.title)
            for book in await book_storage.get_books(**filters)
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation(  # (декоратор, объявляющий поле метода)
        description="""Создать книгу
        - input: BookCreateInput - Данные для создания

        - BookCreateInput: {
            - title: str - Название книги
        }
        """
        )
    @manager.notify(
        "[INFO] GraphQL: Создание книги",
        "book_updates"
        )  # См. Websocket API
    @manager.notify(
        """[INFO] GraphQL: Создание книги:
            function: {func_name},
            input: {input},
            return: {result},
            error: {error}
        """,
        "admin_notifications"
        )  # См. Websocket API
    async def add_book(self, input: BookCreateInput) -> BookType:
        book = BookModel(title=input.title)
        await book_storage.add_book(book)
        return BookType.from_model(book)

    @strawberry.mutation(
        description="""Обновить книгу по ID
        - id: int - Идентификатор книги
        - input: BookUpdateInput - Данные для обновления

        - BookUpdateInput: {
            - title: str - Название книги
        }
        """)
    @manager.notify(
        "[INFO] GraphQL: Обновление книги",
        "book_updates"
        )  # См. Websocket API
    @manager.notify(
        """[INFO] GraphQL: Обновление книги:
            function: {func_name},
            id: {id},
            input: {input},
            return: {result},
            error: {error}
        """,
        "admin_notifications"
        )  # См. Websocket API
    async def update_book(
        self,
        id: strawberry.ID,
        input: BookUpdateInput
    ) -> BookType | None:
        book = await book_storage.update_book(int(id), input.title)
        return BookType.from_model(book) if book else None

    @strawberry.mutation(
        description="""Удалить книгу по ID
        - id: int - Идентификатор книги
        """
        )
    @manager.notify(
        "[INFO] GraphQL: Удаление книги",
        "book_updates"
        )  # См. Websocket API
    @manager.notify(
        """[INFO] GraphQL: Удаление книги:
            function: {func_name},
            id: {id},
            return: {result},
            error: {error}
        """,
        "admin_notifications"
        )  # См. Websocket API
    async def delete_book(self, id: int) -> bool:
        return await book_storage.delete_book(int(id))


schema = strawberry.Schema(query=Query, mutation=Mutation)
