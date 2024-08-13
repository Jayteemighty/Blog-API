from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostResponse(BaseModel):
    id: UUID
    title: str
    content: str
    author: UUID
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
