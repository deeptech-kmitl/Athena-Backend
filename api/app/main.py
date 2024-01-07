from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routers import auth, user, file, book

from database.engine import Base, engine

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = []

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(file.router)
app.include_router(book.router)


@app.get("/")
async def root():
    return {"message": "success"}
