"""Pydantic models for JSONPlaceholder User API responses."""

from __future__ import annotations

from pydantic import BaseModel, field_validator


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    """Single user resource from /users endpoint."""

    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v


class UserCreate(BaseModel):
    """Payload for creating a new user."""

    name: str
    username: str
    email: str
    phone: str | None = None
    website: str | None = None


class UserUpdate(BaseModel):
    """Payload for full user update (PUT)."""

    name: str
    username: str
    email: str
    phone: str | None = None
    website: str | None = None


class UserPatch(BaseModel):
    """Payload for partial user update (PATCH)."""

    name: str | None = None
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    website: str | None = None
