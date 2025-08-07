# 📘 API Styles — Многостилевой API-сервис управления книгами

Данный проект демонстрирует реализацию и сравнение **пяти популярных стилей API** на примере одного сервиса:

- **REST** (FastAPI)
- **GraphQL** (Strawberry GraphQL)
- **gRPC** (Protocol Buffers)
- **WebSocket** (FastAPI)
- **SOAP** (Spyne)

Проект создан **в образовательных целях** — как справочник и учебное пособие для изучения и сравнения различных API-подходов.

---

## ⚙️ Установка и запуск

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/gelubswag/api-styles.git
cd api-styles

# 2. Создайте виртуальное окружение
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.\.venv\Scriptsctivate         # Windows

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Запустите сервер
uvicorn app.main:app --reload
```

---

## 🔌 Доступные интерфейсы

| API-стиль  | Описание                       | URL                                      |
|------------|--------------------------------|------------------------------------------|
| REST       | Swagger UI                     | http://localhost:8000/rest/docs          |
| GraphQL    | GraphQL IDE                    | http://localhost:8000/graphql            |
| gRPC       | Сервер                         | grpc://localhost:50051                   |
| WebSocket  | Уведомления в реальном времени | http://localhost:8000/websocket          |
| SOAP       | XML-интерфейс + WSDL           | http://localhost:8001 + ?wsdl            |

---

## 🧪 Postman-коллекции

- [SOAP API (Postman)](https://www.postman.com/gelub/api-styles/collection/cr2ys54/soap-api?action=share&source=copy-link&creator=39887451)
- [gRPC API (Postman)](https://www.postman.com/gelub/api-styles/collection/6894ee431a70e08ff3d2561e?action=share&source=copy-link&creator=39887451)

---

## 💡 Возможности

- Асинхронное хранилище книг с поддержкой фильтрации
- API-интерфейсы на разных протоколах (HTTP, WebSocket, gRPC)
- Интеграция между API через систему уведомлений WebSocket
- SOAP-интерфейс с генерацией WSDL-контракта
- Веб-интерфейс для тестирования WebSocket API
- Табличное сравнение подходов в статье (см. [API - стили.docx](https://github.com/user-attachments/files/21673932/API.-.docx))

---

## 🎯 Цель проекта

Помочь разработчикам понять различия между архитектурными стилями API и научиться:

- Работать с REST, GraphQL, gRPC, SOAP и WebSocket
- Выбирать подходящий API под задачу
- Строить совместимую и расширяемую архитектуру

---

## 🛠 Технологии

- Python 3.11+
- FastAPI, Strawberry GraphQL, Spyne
- gRPC, Protocol Buffers
- Uvicorn, Pydantic

---

## 🧾 Лицензия

MIT License. Проект предназначен **для обучения** и свободного использования.
