from threading import Thread

from fastapi import FastAPI

from app.rest_api.endpoints import router as book_rest_router
from app.graphql_api.endpoints import router as book_graphql_router
from app.websocket_api.endpoints import router as book_websocket_router
from app.grpc_api.service import serve as grpc_serve
from app.soap_api.service import serve as soap_serve

# Инициализация API
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Запуск gRPC и SOAP сервера в фоне
    global grpc_server
    grpc_server = grpc_serve()
    await grpc_server.start()
    print("gRPC сервер запущен: grpc://localhost:50051")

    global soap_server, soap_thread
    soap_server = soap_serve()
    soap_thread = Thread(target=soap_server.serve_forever, daemon=True)
    soap_thread.start()
    print("SOAP сервер запущен: http://localhost:8001")


@app.on_event("shutdown")
async def shutdown_event():
    # Остановка gRPC сервера
    await grpc_server.stop(0)
    print("gRPC сервер остановлен")
    soap_server.server_close()
    print("SOAP сервер остановлен")
# Подключение роутеров для работы с книгами

# REST API
app.include_router(
    book_rest_router, prefix="/rest", tags=["REST API"]
    )

# GraphQL API
app.include_router(
    book_graphql_router, prefix="/graphql", tags=["GraphQL API"]
)

#  Websocket API
app.include_router(
    book_websocket_router, prefix="/websocket", tags=["Websocket API"]
)
