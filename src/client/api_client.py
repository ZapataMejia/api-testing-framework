"""Base API client with request methods, auth, logging, and response validation."""

from __future__ import annotations

from typing import Any

import requests

from src.client.auth import AuthHandler, AuthType
from src.helpers.logger import log_request, log_response


class APIClient:
    """HTTP client tailored for REST API testing.

    Provides convenience methods for every HTTP verb, automatic header
    management, authentication injection, and structured request/response
    logging.
    """

    def __init__(
        self,
        base_url: str,
        auth_handler: AuthHandler | None = None,
        default_headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout
        self.auth_handler = auth_handler or AuthHandler(AuthType.NONE)
        self.last_response: requests.Response | None = None

        base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if default_headers:
            base_headers.update(default_headers)
        self.session.headers.update(base_headers)

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _merge_headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {**self.auth_handler.get_auth_headers()}
        if extra:
            headers.update(extra)
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        data: Any | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)

        start = log_request(method, url, headers=merged_headers, json=json, params=params)

        response = self.session.request(
            method=method,
            url=url,
            headers=merged_headers,
            params=params,
            json=json,
            data=data,
            timeout=self.timeout,
            **kwargs,
        )

        log_response(response, start)
        self.last_response = response
        return response

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a GET request."""
        return self._request("GET", endpoint, headers=headers, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        json: Any | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a POST request."""
        return self._request("POST", endpoint, headers=headers, json=json, data=data, **kwargs)

    def put(
        self,
        endpoint: str,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a PUT request."""
        return self._request("PUT", endpoint, headers=headers, json=json, **kwargs)

    def patch(
        self,
        endpoint: str,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a PATCH request."""
        return self._request("PATCH", endpoint, headers=headers, json=json, **kwargs)

    def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a DELETE request."""
        return self._request("DELETE", endpoint, headers=headers, **kwargs)
