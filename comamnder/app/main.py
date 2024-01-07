from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import book, user, file

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "https://stackpython.co"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book.router)
app.include_router(user.router)
app.include_router(file.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}