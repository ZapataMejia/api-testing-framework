"""Tests for /comments endpoints on JSONPlaceholder."""

from __future__ import annotations

import pytest

from src.client.api_client import APIClient
from src.helpers.assertions import assert_status
from src.models.post import Comment


@pytest.mark.api
class TestGetComments:
    """GET /comments – retrieval and filtering."""

    def test_get_all_comments(self, api_client: APIClient) -> None:
        """Should return 500 comments total."""
        response = api_client.get("/comments")
        assert_status(response, 200)
        data = response.json()
        assert len(data) == 500

    def test_get_comments_by_post_id(self, api_client: APIClient) -> None:
        """Should filter comments by postId query param."""
        response = api_client.get("/comments", params={"postId": 1})
        assert_status(response, 200)
        comments = [Comment(**c) for c in response.json()]
        assert len(comments) == 5
        assert all(c.postId == 1 for c in comments)


@pytest.mark.api
class TestCreateComment:
    """POST /comments – resource creation."""

    def test_create_comment(self, api_client: APIClient, new_comment_payload: dict) -> None:
        """Should create a comment and return it with an assigned id."""
        response = api_client.post("/comments", json=new_comment_payload)
        assert_status(response, 201)
        data = response.json()
        assert "id" in data
        assert data["email"] == new_comment_payload["email"]


@pytest.mark.api
class TestCommentValidation:
    """Validate comment data integrity."""

    def test_comment_emails_are_valid(self, api_client: APIClient) -> None:
        """All comments for post 1 should have valid email addresses."""
        response = api_client.get("/comments", params={"postId": 1})
        assert_status(response, 200)
        for comment in response.json():
            assert "@" in comment["email"], f"Invalid email: {comment['email']}"
