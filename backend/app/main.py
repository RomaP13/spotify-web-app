from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.main import api_router
from app.api.middlewares import LoggingMiddleware
from app.core.database import create_db_and_tables

# Configure logging
logger.add(
    "logs/debug.log", rotation="10 MB", retention="40 days", level="INFO"
)

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    logger.info("🚀 FastAPI server is starting...")
