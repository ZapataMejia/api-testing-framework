"""JSON schema validation tests for each major endpoint."""

from __future__ import annotations

from typing import Any

import pytest

from src.client.api_client import APIClient
from src.helpers.assertions import assert_json_schema, assert_status


@pytest.mark.schema
class TestSchemaValidation:
    """Validate that API responses conform to their JSON schemas."""

    def test_users_schema(self, api_client: APIClient, user_schema: dict[str, Any]) -> None:
        """Every user in GET /users must match the user JSON schema."""
        response = api_client.get("/users")
        assert_status(response, 200)
        assert_json_schema(response, user_schema)

    def test_single_user_schema(self, api_client: APIClient, user_schema: dict[str, Any]) -> None:
        """GET /users/1 must match the user JSON schema."""
        response = api_client.get("/users/1")
        assert_status(response, 200)
        assert_json_schema(response, user_schema)

    def test_posts_schema(self, api_client: APIClient, post_schema: dict[str, Any]) -> None:
        """Every post in GET /posts must match the post JSON schema."""
        response = api_client.get("/posts")
        assert_status(response, 200)
        assert_json_schema(response, post_schema)

    def test_comments_schema(self, api_client: APIClient, comment_schema: dict[str, Any]) -> None:
        """Every comment for post 1 must match the comment JSON schema."""
        response = api_client.get("/comments", params={"postId": 1})
        assert_status(response, 200)
        assert_json_schema(response, comment_schema)
