"""Pydantic models for JSONPlaceholder Post and Comment API responses."""

from __future__ import annotations

from pydantic import BaseModel


class Post(BaseModel):
    """Single post resource from /posts endpoint."""

    userId: int
    id: int
    title: str
    body: str


class PostCreate(BaseModel):
    """Payload for creating a new post."""

    userId: int
    title: str
    body: str


class PostUpdate(BaseModel):
    """Payload for full post update (PUT)."""

    userId: int
    title: str
    body: str


class Comment(BaseModel):
    """Single comment resource from /comments endpoint."""

    postId: int
    id: int
    name: str
    email: str
    body: str


class CommentCreate(BaseModel):
    """Payload for creating a new comment."""

    postId: int
    name: str
    email: str
    body: str
