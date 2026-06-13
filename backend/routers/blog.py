import aiofiles
from fastapi import APIRouter, HTTPException
from models.blog import BlogPost
from services.blog_store import load_posts

router = APIRouter()


@router.get("/blog", response_model=list[BlogPost])
async def get_posts(limit: int = 20, category: str = ""):
    posts = await load_posts()
    if category:
        posts = [p for p in posts if p.category.lower() == category.lower()]
    posts.sort(key=lambda p: p.date, reverse=True)
    return posts[:limit]


@router.get("/blog/featured", response_model=list[BlogPost])
async def get_featured(limit: int = 3):
    posts = await load_posts()
    featured = [p for p in posts if p.featured]
    featured.sort(key=lambda p: p.date, reverse=True)
    return featured[:limit]


@router.get("/blog/{slug}", response_model=BlogPost)
async def get_post(slug: str):
    posts = await load_posts()
    for post in posts:
        if post.slug == slug:
            return post
    raise HTTPException(status_code=404, detail="Post not found")
