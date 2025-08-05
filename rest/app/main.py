from fastapi import FastAPI
from api.endpoints import router as book_router


app = FastAPI()
app.include_router(book_router)
