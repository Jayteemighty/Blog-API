from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogPostSchema(BaseModel):
    title: str
    content: str
    author_id: int

class BlogPostResponseSchema(BlogPostSchema):
    id: int
    created_at: datetime
    updated_at: datetime
