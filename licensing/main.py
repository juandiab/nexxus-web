import asyncio
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router as auth_router
from config import settings
from crypto import _get_fernet
from db import close_database, ping_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [licensing] %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Nexxus Tech Licensing API",
    description="License management and activation API",
    version="0.5.0",
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
    try:
        _get_fernet()
        logger.info("ENCRYPTION_KEY validated")
    except ValueError as exc:
        logger.error("%s", exc)
        raise

    for attempt in range(1, 16):
        try:
            await ping_database()
            logger.info("MongoDB connected")
            return
        except Exception as exc:
            logger.warning("MongoDB not ready (attempt %s/15): %s", attempt, exc)
            await asyncio.sleep(2)

    logger.warning(
        "MongoDB unavailable after 30s; starting anyway (health will show degraded)"
    )


@app.on_event("shutdown")
async def shutdown():
    await close_database()


@app.get("/health")
async def health():
    mongo_ok = False
    try:
        mongo_ok = await ping_database()
    except Exception as exc:
        logger.debug("Health check MongoDB ping failed: %s", exc)
    return {
        "status": "ok" if mongo_ok else "degraded",
        "service": "nexxus-tech-licensing",
        "mongodb": "connected" if mongo_ok else "unavailable",
    }
