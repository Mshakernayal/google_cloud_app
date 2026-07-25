from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str | None = None
    author: str
    published: bool = False


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None
    published: bool | None = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str | None
    author: str
    published: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedPosts(BaseModel):
    count: int
    posts: list[PostResponse]
