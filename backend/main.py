from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import contact, blog, blog_admin, chat, chat_admin

app = FastAPI(
    title="Nexxus Tech API",
    description="Backend API for nexxus-tech.com",
    version="1.0.0",
    docs_url="/api/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

origins = [o.strip() for o in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(contact.router, prefix="/api")
app.include_router(blog.router, prefix="/api")
app.include_router(blog_admin.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(chat_admin.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "nexxus-tech-api"}
