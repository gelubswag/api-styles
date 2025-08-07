# [file name]: app/soap_api/service.py
from spyne import Application, ServiceBase, rpc
from spyne import Integer, Unicode, Iterable, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from app.soap_api.models import BookSOAP
from app.core.sotrage_sync import book_storage, BookModel


class BookServiceSOAP(ServiceBase):
    @rpc(Unicode, _returns=BookSOAP)
    def AddBook(ctx, title):
        """Добавление новой книги через SOAP"""
        book = BookModel(title=title)
        book_storage.add_book(book)
        return BookSOAP(id=book.id, title=book.title)

    @rpc(_returns=Iterable(BookSOAP))
    def GetBooks(ctx):
        """Получение списка книг через SOAP"""
        books = book_storage.get_books()
        return [BookSOAP(id=b.id, title=b.title) for b in books]

    @rpc(Integer, _returns=BookSOAP)
    def GetBook(ctx, id):
        """Получение книги по ID через SOAP"""
        book = book_storage.get_book(id=id)
        return BookSOAP(id=book.id, title=book.title) if book else None

    @rpc(Integer, Unicode, _returns=BookSOAP)
    def UpdateBook(ctx, id, title):
        """Обновление книги по ID через SOAP"""
        book = book_storage.update_book(book_id=id, title=title)
        return BookSOAP(id=book.id, title=book.title) if book else None

    @rpc(Integer, _returns=Boolean)
    def DeleteBook(ctx, id):
        """Удаление книги по ID через SOAP"""
        return book_storage.delete_book(book_id=id)


def serve():
    """Запуск SOAP сервера"""
    application = Application(
        [BookServiceSOAP],
        'book_service',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )
    application.transport = 'http://schemas.xmlsoap.org/soap/http'
    application.interface.types_style = 'pretty'
    application.interface.docs_style = 'restructured'

    wsgi_application = WsgiApplication(application)
    server = make_server('localhost', 8001, wsgi_application)
    return server
