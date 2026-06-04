import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router as auth_router
from config import settings
from crypto import _get_fernet
from db import close_database, ping_database

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Nexxus Tech Licensing API",
    description="License management and activation API",
    version="0.1.0",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    _get_fernet()
    await ping_database()
    logger.info("Licensing service started; MongoDB connection OK")


@app.on_event("shutdown")
async def shutdown():
    await close_database()


@app.get("/health")
async def health():
    mongo_ok = await ping_database()
    return {
        "status": "ok" if mongo_ok else "degraded",
        "service": "nexxus-tech-licensing",
        "mongodb": "connected" if mongo_ok else "unavailable",
    }
