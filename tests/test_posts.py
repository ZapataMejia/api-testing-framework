"""Tests for /posts endpoints on JSONPlaceholder."""

from __future__ import annotations

import pytest

from src.client.api_client import APIClient
from src.helpers.assertions import assert_list_length, assert_status
from src.models.post import Comment, Post


@pytest.mark.smoke
@pytest.mark.api
class TestGetPosts:
    """GET /posts – listing, single retrieval, and filtering."""

    def test_get_all_posts(self, api_client: APIClient) -> None:
        """Should return 100 posts."""
        response = api_client.get("/posts")
        assert_status(response, 200)
        assert_list_length(response, 100)

    def test_get_single_post(self, api_client: APIClient) -> None:
        """Should return post id=1 with correct userId."""
        response = api_client.get("/posts/1")
        assert_status(response, 200)
        post = Post(**response.json())
        assert post.id == 1
        assert post.userId == 1

    def test_filter_posts_by_user(self, api_client: APIClient) -> None:
        """Should filter posts for userId=1 (10 posts)."""
        response = api_client.get("/posts", params={"userId": 1})
        assert_status(response, 200)
        data = response.json()
        assert len(data) == 10
        assert all(p["userId"] == 1 for p in data)


@pytest.mark.api
class TestCreatePost:
    """POST /posts – resource creation."""

    def test_create_post(self, api_client: APIClient, new_post_payload: dict) -> None:
        """Should create a post and return it with an assigned id."""
        response = api_client.post("/posts", json=new_post_payload)
        assert_status(response, 201)
        data = response.json()
        assert "id" in data
        assert data["title"] == new_post_payload["title"]


@pytest.mark.regression
@pytest.mark.api
class TestUpdatePost:
    """PUT /posts – full update."""

    def test_put_update_post(self, api_client: APIClient, new_post_payload: dict) -> None:
        """PUT should replace the entire post resource."""
        response = api_client.put("/posts/1", json=new_post_payload)
        assert_status(response, 200)
        assert response.json()["title"] == new_post_payload["title"]


@pytest.mark.smoke
@pytest.mark.api
class TestPostComments:
    """GET /posts/{id}/comments – nested resource."""

    def test_get_comments_for_post(self, api_client: APIClient) -> None:
        """Should return 5 comments for post id=1."""
        response = api_client.get("/posts/1/comments")
        assert_status(response, 200)
        comments = [Comment(**c) for c in response.json()]
        assert len(comments) == 5
        assert all(c.postId == 1 for c in comments)
