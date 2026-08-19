from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .database import Base, engine
from . import models

app = FastAPI(
    title="Phonebook API",
    description="A simple phonebook application API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(router)
@app.get("/")
def home():
    return {
        "message": "Phonebook API is running"
    }