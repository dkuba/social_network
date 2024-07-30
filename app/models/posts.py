from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Post(BaseModel):
    """Модель поста."""

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)
    post_text: str


class PostRead(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    post_text: str


class PostCreate(BaseModel):
    text: str
