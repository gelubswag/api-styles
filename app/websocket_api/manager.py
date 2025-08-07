from asyncio import run
from functools import wraps


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, set] = {
            "book_updates": set(),
            "admin_notifications": set()
        }

    async def connect(self, websocket, channel: str):
        """Регистрируем новое подключение к каналу"""
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)

    def disconnect(self, websocket, channel: str):
        """Удаляем подключение из канала"""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)

    async def send_personal_message(self, message: str, websocket):
        """Отправляем сообщение конкретному подключению"""
        await websocket.send_text(message)

    async def broadcast(self, message: str, channel: str):
        """Отправляем сообщение всем подписчикам канала"""
        if channel in self.active_connections:
            for connection in self.active_connections[channel]:
                await connection.send_text(message)

    def broadcast_sync(self, message: str, channel: str):
        """Отправляем сообщение всем подписчикам канала"""
        if channel in self.active_connections:
            for connection in self.active_connections[channel]:
                run(connection.send_text(message))

    def notify(self, message: str, channel: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    result = await func(*args, **kwargs)
                    await self.broadcast(
                        message.format(
                            *args, **kwargs | {
                                'channel': channel,
                                'message': message,
                                'result': result,
                                'args': args,
                                'kwargs': kwargs,
                                'func_name': func.__name__,
                                'error': None
                                }
                            ), channel)
                    return result
                except Exception as e:
                    await self.broadcast(
                        message.format(
                            *args, **kwargs | {
                                'channel': channel,
                                'message': message,
                                'result': e,
                                'args': args,
                                'kwargs': kwargs,
                                'func_name': func.__name__,
                                'error': e
                                }
                            ), channel)
                    raise e
            return wrapper
        return decorator


manager = ConnectionManager()
