from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    username: str
    first_name: str
    last_name: str
    phone_number: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    access: str
    refresh: str

class ProfileSchema(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone_number: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
