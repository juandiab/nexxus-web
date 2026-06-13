from pydantic import BaseModel, Field


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
    cover_color: str = "#007BA7"


class BlogPostWrite(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    slug: str = Field(default="", max_length=256)
    excerpt: str = Field(default="", max_length=500)
    content: str = Field(min_length=1)
    category: str = Field(min_length=1, max_length=128)
    tags: list[str] = Field(default_factory=list)
    author: str = Field(min_length=1, max_length=128)
    author_role: str = Field(min_length=1, max_length=128)
    date: str = Field(default="", max_length=32)
    read_time: int | None = Field(default=None, ge=1, le=120)
    featured: bool = False
    cover_color: str = Field(default="#007BA7", max_length=32)


class BlogAssistRequest(BaseModel):
    draft: str = Field(min_length=50, max_length=50000)


class BlogAssistResponse(BaseModel):
    title: str
    slug: str
    excerpt: str
    category: str
    tags: list[str]
    read_time: int
    cover_color: str
    content: str
