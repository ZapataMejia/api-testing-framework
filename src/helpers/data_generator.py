"""Faker-based test data generation for API payloads."""

from __future__ import annotations

from faker import Faker

fake = Faker()


def random_user() -> dict[str, str]:
    """Generate a random user payload compatible with JSONPlaceholder."""
    return {
        "name": fake.name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "website": fake.domain_name(),
    }


def random_post(user_id: int = 1) -> dict[str, str | int]:
    """Generate a random post payload."""
    return {
        "userId": user_id,
        "title": fake.sentence(nb_words=6),
        "body": fake.paragraph(nb_sentences=3),
    }


def random_comment(post_id: int = 1) -> dict[str, str | int]:
    """Generate a random comment payload."""
    return {
        "postId": post_id,
        "name": fake.sentence(nb_words=4),
        "email": fake.email(),
        "body": fake.paragraph(nb_sentences=2),
    }


def random_email() -> str:
    return fake.email()


def random_name() -> str:
    return fake.name()
