"""Root conftest: global fixtures and pytest hooks."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv()

SCHEMA_DIR = Path(__file__).parent / "schemas"


def pytest_configure(config: pytest.Config) -> None:
    """Inject metadata into the HTML report."""
    config.stash.setdefault(pytest.StashKey[str](), "api-testing-framework")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Automatically tag tests based on their module path."""
    for item in items:
        if "performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        if "schema_validation" in item.nodeid:
            item.add_marker(pytest.mark.schema)


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def user_schema() -> dict:
    return json.loads((SCHEMA_DIR / "user.json").read_text())


@pytest.fixture(scope="session")
def post_schema() -> dict:
    return json.loads((SCHEMA_DIR / "post.json").read_text())


@pytest.fixture(scope="session")
def comment_schema() -> dict:
    return json.loads((SCHEMA_DIR / "comment.json").read_text())
