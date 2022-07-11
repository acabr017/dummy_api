from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime
from typing import Optional

from app.database import Base
# This is a schema model/pydantic model
# =========================================================================================
# User Stuff


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =========================================================================================
# Post Stuff


class Post(BaseModel):
    # The Schema we want: title (str), content (str)
    title: str
    content: str
    # Providing an optional field that defaults to given
    published: bool = True
    # Providing an optional field that defaults to None
    # rating: Optional[int] = None


class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    # This is necessary when using the ORM, as it doens't recognize the type otherwise

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


# =========================================================================================
# Token Stuff

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

# =========================================================================================
# Token Stuff


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
