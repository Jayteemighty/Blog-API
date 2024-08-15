from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BlogPostSchema(BaseModel):
    title: str
    content: str
    author_id: UUID

class BlogPostResponseSchema(BlogPostSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
