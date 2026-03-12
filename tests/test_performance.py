"""Performance tests: response time assertions and concurrent requests."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from src.client.api_client import APIClient
from src.helpers.assertions import assert_response_time, assert_status


@pytest.mark.performance
class TestPerformance:
    """Measure response times and concurrency behaviour."""

    def test_single_user_response_time(self, api_client: APIClient) -> None:
        """GET /users/1 should respond within 2 seconds."""
        response = api_client.get("/users/1")
        assert_status(response, 200)
        assert_response_time(response, max_ms=2000)

    def test_all_posts_response_time(self, api_client: APIClient) -> None:
        """GET /posts (100 items) should respond within 3 seconds."""
        response = api_client.get("/posts")
        assert_status(response, 200)
        assert_response_time(response, max_ms=3000)

    def test_concurrent_requests(self, api_client: APIClient) -> None:
        """10 concurrent GET requests should all succeed."""
        endpoints = [f"/users/{i}" for i in range(1, 11)]

        def fetch(endpoint: str) -> int:
            resp = api_client.get(endpoint)
            return resp.status_code

        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {pool.submit(fetch, ep): ep for ep in endpoints}
            results = {}
            for future in as_completed(futures):
                ep = futures[future]
                results[ep] = future.result()

        for ep, status in results.items():
            assert status == 200, f"{ep} returned {status}"
