import asyncio
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from crypto import _get_fernet
from db import close_database, get_database, ping_database
from routers.activation import activate_router, router as activation_router
from routers.auth import router as auth_router
from routers.licenses import router as licenses_router
from routers.users import router as users_router
from routers.sync import router as sync_router
from routers.webauthn import router as webauthn_router
from services.activation_service import ensure_activation_pending_indexes
from services.license_service import ensure_license_indexes
from services.user_service import ensure_default_admin, ensure_user_indexes
from services.webauthn_service import ensure_webauthn_indexes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [licensing] %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Nexxus Tech Licensing API",
    description="License management and activation API",
    version="0.7.2",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

origins = settings.cors_origin_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(webauthn_router)
app.include_router(licenses_router)
app.include_router(activation_router)
app.include_router(activate_router)
app.include_router(sync_router)


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
            db = get_database()
            await ensure_user_indexes(db)
            await ensure_webauthn_indexes(db)
            await ensure_license_indexes(db)
            await ensure_activation_pending_indexes(db)
            await ensure_default_admin(db)
            logger.info("MongoDB connected and indexes ready")
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
