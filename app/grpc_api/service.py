import grpc

from app.grpc_api import book_pb2, book_pb2_grpc
from app.core.storage import book_storage, BookModel


class BookService(book_pb2_grpc.BookServiceServicer):
    async def GetBooks(self, request, context):
        filters = {
            'title': request.title or None,
            'id': request.id or None,
            'id__lt': request.id_lt or None,
            'id__gt': request.id_gt or None
        }
        books = await book_storage.get_books(**filters)
        return book_pb2.BooksResponse(books=[
            book_pb2.Book(id=book.id, title=book.title) for book in books
        ])

    async def CreateBook(self, request, context):
        book = BookModel(title=request.title)
        await book_storage.add_book(book)
        return book_pb2.Book(id=book.id, title=book.title)

    async def UpdateBook(self, request, context):
        updated_book = await book_storage.update_book(
            request.id,
            request.title
            )
        if not updated_book:
            context.abort(grpc.StatusCode.NOT_FOUND, "Book not found")
        return book_pb2.Book(id=updated_book.id, title=updated_book.title)

    async def DeleteBook(self, request, context):
        success = await book_storage.delete_book(request.id)
        if not success:
            context.abort(grpc.StatusCode.NOT_FOUND, "Book not found")
        return book_pb2.DeleteResponse(success=True)


def serve():
    server = grpc.aio.server()
    book_pb2_grpc.add_BookServiceServicer_to_server(BookService(), server)
    server.add_insecure_port('[::]:50051')
    return server
