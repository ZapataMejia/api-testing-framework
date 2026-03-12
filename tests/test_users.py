"""Tests for /users endpoints on JSONPlaceholder."""

from __future__ import annotations

import pytest

from src.client.api_client import APIClient
from src.helpers.assertions import assert_contains, assert_list_length, assert_status
from src.models.user import User


@pytest.mark.smoke
@pytest.mark.api
class TestGetUsers:
    """GET /users – list and single resource retrieval."""

    def test_get_all_users(self, api_client: APIClient) -> None:
        """Should return a list of 10 users."""
        response = api_client.get("/users")
        assert_status(response, 200)
        assert_list_length(response, 10)

    def test_get_single_user(self, api_client: APIClient) -> None:
        """Should return user with matching id."""
        response = api_client.get("/users/1")
        assert_status(response, 200)
        user = User(**response.json())
        assert user.id == 1
        assert user.name == "Leanne Graham"

    def test_get_nonexistent_user(self, api_client: APIClient) -> None:
        """Should return 404 for a user that does not exist."""
        response = api_client.get("/users/9999")
        assert_status(response, 404)

    def test_filter_users_by_username(self, api_client: APIClient) -> None:
        """Should filter users using query parameters."""
        response = api_client.get("/users", params={"username": "Bret"})
        assert_status(response, 200)
        data = response.json()
        assert len(data) == 1
        assert data[0]["username"] == "Bret"


@pytest.mark.api
class TestCreateUser:
    """POST /users – resource creation."""

    def test_create_user(self, api_client: APIClient, new_user_payload: dict) -> None:
        """Should create a user and return the payload with an assigned id."""
        response = api_client.post("/users", json=new_user_payload)
        assert_status(response, 201)
        data = response.json()
        assert "id" in data
        assert data["name"] == new_user_payload["name"]
        assert data["email"] == new_user_payload["email"]


@pytest.mark.regression
@pytest.mark.api
class TestUpdateUser:
    """PUT and PATCH /users – full and partial updates."""

    def test_put_update_user(self, api_client: APIClient, new_user_payload: dict) -> None:
        """PUT should replace the entire user resource."""
        response = api_client.put("/users/1", json=new_user_payload)
        assert_status(response, 200)
        data = response.json()
        assert data["name"] == new_user_payload["name"]
        assert data["email"] == new_user_payload["email"]

    def test_patch_partial_update(self, api_client: APIClient) -> None:
        """PATCH should update only the specified fields."""
        patch_data = {"name": "Patched Name"}
        response = api_client.patch("/users/1", json=patch_data)
        assert_status(response, 200)
        assert response.json()["name"] == "Patched Name"


@pytest.mark.api
class TestDeleteUser:
    """DELETE /users – resource removal."""

    def test_delete_user(self, api_client: APIClient) -> None:
        """DELETE should return 200 with empty body."""
        response = api_client.delete("/users/1")
        assert_status(response, 200)
