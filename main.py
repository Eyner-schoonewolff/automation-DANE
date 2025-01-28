# main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from mangum import Mangum
from app.entrypoints import router
import os

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI(title="Lambda Function API", version="1.0")

# CORS
origins = ",".join(
    [
        "http://localhost:3000"
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOWED_ORIGINS", origins).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Este "*" incluye todos los encabezados
)
app.include_router(router.automation)


handler = Mangum(app, lifespan="off")
