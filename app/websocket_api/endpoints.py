from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    templating,
    Request,
    Response
)

from .manager import manager
from .handler import handle_message

router = APIRouter()

templates = templating.Jinja2Templates(directory="app/websocket_api/templates")


@router.websocket("/book-updates")
async def book_updates_websocket(websocket: WebSocket):
    await websocket.accept()
    channel = "book_updates"

    try:
        # Регистрируем подключение
        await manager.connect(websocket, channel)

        # Подтверждение подключения
        await manager.send_personal_message(
            "Подключение установлено", websocket
            )

        # Бесконечный цикл для поддержания соединения
        while True:
            # Можно получать сообщения от клиента, если нужно
            data = await websocket.receive_text()
            print(f"Получено сообщение: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
        await manager.broadcast("Клиент отключился", channel)


@router.websocket("/admin")
async def admin_websocket(websocket: WebSocket):
    await websocket.accept()
    channel = "admin_notifications"

    try:
        await manager.connect(websocket, channel)
        await manager.send_personal_message(
            "Подключение установлено", websocket
            )

        while True:
            data = await websocket.receive_text()
            print(f"Получено сообщение: {data}")
            message = await handle_message(data)
            await manager.broadcast(message, channel)
            print(f"Сообщение отправлено: {message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


@router.get("/")
async def admin(request: Request, response: Response):
    return templates.TemplateResponse(request, "websocket_test.html")
