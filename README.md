# API Testing Framework

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![pytest](https://img.shields.io/badge/pytest-7.4%2B-green?logo=pytest)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

A professional, extensible Python framework for automated REST API testing — built with **pytest**, **requests**, and **Pydantic**.

---

## Architecture

```
api-testing-framework/
├── src/
│   ├── client/
│   │   ├── api_client.py      # Base HTTP client (get/post/put/patch/delete)
│   │   └── auth.py            # Auth strategies (Bearer, API Key, Basic)
│   ├── models/
│   │   ├── user.py            # Pydantic models for User resources
│   │   └── post.py            # Pydantic models for Post & Comment resources
│   └── helpers/
│       ├── assertions.py      # Custom assertion helpers
│       ├── data_generator.py  # Faker-based test data generation
│       └── logger.py          # Structured request/response logging
├── tests/
│   ├── conftest.py            # Fixtures: api_client, auth_client, payloads
│   ├── test_users.py          # 8 tests — CRUD, filter, pagination
│   ├── test_posts.py          # 6 tests — CRUD, filter, nested comments
│   ├── test_comments.py       # 4 tests — GET, POST, validation
│   ├── test_auth.py           # 3 tests — Bearer token, 401/403 mocks
│   ├── test_performance.py    # 3 tests — Response time, concurrency
│   └── test_schema_validation.py  # 4 tests — JSON schema validation
├── schemas/                   # JSON Schema definitions
├── .github/workflows/         # CI/CD pipeline
├── conftest.py                # Root fixtures and hooks
├── pytest.ini                 # Markers and pytest settings
├── Makefile                   # Dev commands
├── Dockerfile                 # Containerised execution
└── requirements.txt
```

## Quick Start

```bash
# Clone & enter
git clone <repo-url> && cd api-testing-framework

# Virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
make install          # or: pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Run all tests
make test
```

## Test Categories

Tests are organized with **pytest markers** so you can run exactly what you need:

| Marker        | Command                | Description                          |
|---------------|------------------------|--------------------------------------|
| `smoke`       | `make test-smoke`      | Critical-path sanity checks          |
| `regression`  | `make test-regression` | Full regression suite                |
| `performance` | `make test-performance`| Response time & concurrency          |
| `schema`      | `make test-schema`     | JSON schema conformance              |
| `api`         | `pytest -m api`        | All standard API contract tests      |
| *(all)*       | `make test`            | Everything with HTML report          |

Run tests in parallel:

```bash
make test-parallel     # uses pytest-xdist (-n auto)
```

## Adding New Tests

1. **Define a Pydantic model** in `src/models/` for the new resource.
2. **Add a JSON schema** in `schemas/` for schema-validation tests.
3. **Create a test file** in `tests/` following the existing pattern:
   - Import `APIClient` and assertion helpers.
   - Use fixtures from `tests/conftest.py`.
   - Decorate with appropriate markers (`@pytest.mark.smoke`, etc.).
4. **Generate test data** via `src/helpers/data_generator.py` using Faker.

Example:

```python
@pytest.mark.smoke
@pytest.mark.api
def test_get_albums(api_client: APIClient) -> None:
    response = api_client.get("/albums")
    assert_status(response, 200)
    assert len(response.json()) == 100
```

## CI/CD

The GitHub Actions workflow (`.github/workflows/api-tests.yml`):

- Runs on **push** and **pull request** to `main`
- Scheduled **weekday runs** at 06:00 UTC
- Tests against Python **3.11** and **3.12**
- Uploads **HTML** and **Allure** reports as artifacts
- Runs **lint** → **smoke** → **full suite**

## Docker

```bash
# Build
docker build -t api-tests .

# Run all tests
docker run --rm api-tests

# Run only smoke tests
docker run --rm api-tests -m smoke
```

## Reports

- **HTML**: `pytest --html=report.html --self-contained-html`
- **Allure**: `make report` (generates and serves Allure report)

## Tech Stack

| Tool          | Purpose                     |
|---------------|-----------------------------|
| pytest        | Test runner & fixtures       |
| requests      | HTTP client                  |
| Pydantic      | Response model validation    |
| Faker         | Test data generation         |
| jsonschema    | JSON Schema validation       |
| pytest-html   | HTML test reports            |
| pytest-xdist  | Parallel test execution      |
| allure-pytest | Rich reporting               |
| ruff          | Linting & formatting         |
| python-dotenv | Environment configuration    |
