from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    return get_client().get_default_database()


async def ping_database() -> bool:
    await get_client().admin.command("ping")
    return True


async def close_database() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
