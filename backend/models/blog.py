from pydantic import BaseModel
from typing import Optional


class BlogPost(BaseModel):
    id: str
    slug: str
    title: str
    excerpt: str
    content: str
    category: str
    tags: list[str]
    author: str
    author_role: str
    date: str
    read_time: int
    featured: bool = False
    cover_color: str = "#5B4FE8"
