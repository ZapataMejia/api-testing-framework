"""Tests for authentication handling (mocked scenarios)."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.client.api_client import APIClient
from src.client.auth import AuthHandler, AuthType
from src.helpers.assertions import assert_status


def _mock_response(status: int, text: str, url: str) -> MagicMock:
    """Build a mock requests.Response with all attributes the framework reads."""
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status
    resp.text = text
    resp.url = url
    resp.elapsed = timedelta(milliseconds=50)
    resp.request = MagicMock()
    resp.request.method = "GET"
    return resp


@pytest.mark.api
class TestAuthentication:
    """Verify auth header injection and error handling.

    JSONPlaceholder does not enforce authentication, so we mock
    responses to simulate real auth flows.
    """

    def test_bearer_token_sent_in_header(self, auth_client: APIClient) -> None:
        """Authenticated client should send Authorization header on every request."""
        response = auth_client.get("/users/1")
        assert_status(response, 200)
        sent_headers = response.request.headers
        assert "Authorization" in sent_headers
        assert sent_headers["Authorization"].startswith("Bearer ")

    @patch("src.client.api_client.requests.Session.request")
    def test_invalid_token_returns_401(self, mock_request: MagicMock, base_url: str) -> None:
        """Simulate a 401 response for an invalid bearer token."""
        mock_request.return_value = _mock_response(401, '{"error": "Invalid token"}', f"{base_url}/users")

        handler = AuthHandler(auth_type=AuthType.BEARER, token="invalid-token")
        client = APIClient(base_url=base_url, auth_handler=handler)
        response = client.get("/users")
        assert_status(response, 401)

    @patch("src.client.api_client.requests.Session.request")
    def test_expired_token_returns_403(self, mock_request: MagicMock, base_url: str) -> None:
        """Simulate a 403 response for an expired token."""
        mock_request.return_value = _mock_response(403, '{"error": "Token expired"}', f"{base_url}/users")

        handler = AuthHandler(auth_type=AuthType.BEARER, token="expired-token")
        client = APIClient(base_url=base_url, auth_handler=handler)
        response = client.get("/users")
        assert_status(response, 403)
