"""Test-level fixtures: api client, auth client, and test data generators."""

from __future__ import annotations

import pytest

from src.client.api_client import APIClient
from src.client.auth import AuthHandler, AuthType
from src.helpers.data_generator import random_comment, random_post, random_user


@pytest.fixture(scope="session")
def api_client(base_url: str) -> APIClient:
    """Unauthenticated API client for public endpoints."""
    return APIClient(base_url=base_url)


@pytest.fixture(scope="session")
def auth_client(base_url: str) -> APIClient:
    """API client with bearer-token authentication."""
    handler = AuthHandler(auth_type=AuthType.BEARER, token="test-token-abc123")
    return APIClient(base_url=base_url, auth_handler=handler)


@pytest.fixture()
def new_user_payload() -> dict:
    """Fresh random user payload for each test."""
    return random_user()


@pytest.fixture()
def new_post_payload() -> dict:
    """Fresh random post payload for each test."""
    return random_post()


@pytest.fixture()
def new_comment_payload() -> dict:
    """Fresh random comment payload for each test."""
    return random_comment()
