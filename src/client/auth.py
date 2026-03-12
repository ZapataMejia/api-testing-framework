"""Authentication handler supporting multiple auth strategies."""

from __future__ import annotations

import base64
from enum import Enum
from typing import Any


class AuthType(Enum):
    BEARER = "bearer"
    API_KEY = "api_key"
    BASIC = "basic"
    NONE = "none"


class AuthHandler:
    """Manages authentication headers for API requests."""

    def __init__(
        self,
        auth_type: AuthType = AuthType.NONE,
        token: str | None = None,
        api_key: str | None = None,
        api_key_header: str = "X-API-Key",
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        self._auth_type = auth_type
        self._token = token
        self._api_key = api_key
        self._api_key_header = api_key_header
        self._username = username
        self._password = password

    def get_auth_headers(self) -> dict[str, str]:
        """Return authentication headers based on configured strategy."""
        match self._auth_type:
            case AuthType.BEARER:
                if not self._token:
                    raise ValueError("Bearer token is required")
                return {"Authorization": f"Bearer {self._token}"}
            case AuthType.API_KEY:
                if not self._api_key:
                    raise ValueError("API key is required")
                return {self._api_key_header: self._api_key}
            case AuthType.BASIC:
                if not self._username or not self._password:
                    raise ValueError("Username and password are required")
                credentials = base64.b64encode(
                    f"{self._username}:{self._password}".encode()
                ).decode()
                return {"Authorization": f"Basic {credentials}"}
            case AuthType.NONE:
                return {}

    def update_token(self, token: str) -> None:
        """Replace the current bearer token."""
        self._token = token

    def to_dict(self) -> dict[str, Any]:
        """Serialize auth config (tokens redacted)."""
        return {
            "auth_type": self._auth_type.value,
            "has_token": self._token is not None,
            "has_api_key": self._api_key is not None,
        }
