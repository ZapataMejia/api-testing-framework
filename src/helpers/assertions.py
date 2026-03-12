"""Custom assertion helpers for API response validation."""

from __future__ import annotations

from typing import Any

import jsonschema
import requests


def assert_status(response: requests.Response, expected: int) -> None:
    """Assert the HTTP status code matches the expected value."""
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}. "
        f"Body: {response.text[:300]}"
    )


def assert_status_in(response: requests.Response, expected: set[int]) -> None:
    """Assert the status code is one of the expected values."""
    assert response.status_code in expected, (
        f"Expected status in {expected}, got {response.status_code}"
    )


def assert_json_schema(response: requests.Response, schema: dict[str, Any]) -> None:
    """Validate response JSON against a JSON Schema."""
    data = response.json()
    if isinstance(data, list):
        for item in data:
            jsonschema.validate(instance=item, schema=schema)
    else:
        jsonschema.validate(instance=data, schema=schema)


def assert_response_time(response: requests.Response, max_ms: float) -> None:
    """Assert the response was received within the given time budget."""
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms <= max_ms, (
        f"Response took {elapsed_ms:.0f}ms, exceeding limit of {max_ms:.0f}ms"
    )


def assert_contains(response: requests.Response, key: str, value: Any | None = None) -> None:
    """Assert the response JSON contains the given key, optionally with a specific value."""
    data = response.json()
    if isinstance(data, list):
        data = data[0] if data else {}
    assert key in data, f"Key '{key}' not found in response. Keys: {list(data.keys())}"
    if value is not None:
        assert data[key] == value, f"Expected {key}={value!r}, got {data[key]!r}"


def assert_list_length(response: requests.Response, expected: int) -> None:
    """Assert that the response JSON array has the expected length."""
    data = response.json()
    assert isinstance(data, list), f"Expected list response, got {type(data).__name__}"
    assert len(data) == expected, f"Expected {expected} items, got {len(data)}"


def assert_sorted(response: requests.Response, key: str, reverse: bool = False) -> None:
    """Assert the response list is sorted by a given key."""
    data = response.json()
    values = [item[key] for item in data]
    assert values == sorted(values, reverse=reverse), (
        f"Response not sorted by '{key}' ({'desc' if reverse else 'asc'})"
    )
