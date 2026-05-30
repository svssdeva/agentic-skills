<!-- Source: https://www.skills.sh/wshobson/agents/python-testing-patterns -->
<!-- Install: npx skills add https://github.com/wshobson/agents --skill python-testing-patterns -->
---
name: python-testing-patterns
description: Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices.
---

# Python Testing Patterns

Comprehensive guide to implementing robust testing strategies in Python using pytest, fixtures, mocking, parameterization, and test-driven development practices.

## When to Use This Skill

- Writing unit tests for Python code
- Setting up test suites and test infrastructure
- Implementing test-driven development (TDD)
- Creating integration tests for APIs and services
- Mocking external dependencies and services
- Testing async code and concurrent operations
- Setting up continuous testing in CI/CD
- Implementing property-based testing
- Testing database operations
- Debugging failing tests

## Core Concepts

- **Test Types**: Unit (isolation), Integration (components), Functional (features), Performance (speed)
- **AAA Pattern**: Arrange → Act → Assert
- **Test Isolation**: Independent tests, no shared state, clean up after each

## Fundamental Patterns

### Pattern 1: Basic pytest Tests

```python
import pytest

def test_addition():
    assert add(2, 3) == 5

def test_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)
```

### Pattern 2: Fixtures for Setup and Teardown

```python
@pytest.fixture
def db() -> Generator[Database, None, None]:
    database = Database("sqlite:///:memory:")
    database.connect()
    yield database
    database.disconnect()

@pytest.fixture(scope="session")
def app_config():
    return {"database_url": "postgresql://localhost/test", "debug": True}
```

Fixture scopes: `function` (default), `class`, `module`, `session`.

### Pattern 3: Parameterized Tests

```python
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("", False),
])
def test_email_validation(email, expected):
    assert is_valid_email(email) == expected

# Custom IDs
@pytest.mark.parametrize("value,expected", [
    pytest.param(1, True, id="positive"),
    pytest.param(0, False, id="zero"),
    pytest.param(-1, False, id="negative"),
])
def test_is_positive(value, expected):
    assert (value > 0) == expected
```

### Pattern 4: Mocking with unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

def test_get_user_success():
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        user = client.get_user(1)
        assert user["id"] == 1
        mock_get.assert_called_once_with("https://api.example.com/users/1")

def test_get_user_not_found():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404")
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            client.get_user(999)
```

### Pattern 5: Testing Retry Behavior

```python
def test_retries_on_transient_error():
    client = Mock()
    client.request.side_effect = [
        ConnectionError("Failed"),
        ConnectionError("Failed"),
        {"status": "ok"},
    ]
    service = ServiceWithRetry(client, max_retries=3)
    result = service.fetch()
    assert result == {"status": "ok"}
    assert client.request.call_count == 3

def test_gives_up_after_max_retries():
    client = Mock()
    client.request.side_effect = ConnectionError("Failed")
    service = ServiceWithRetry(client, max_retries=3)
    with pytest.raises(ConnectionError):
        service.fetch()
    assert client.request.call_count == 3

def test_does_not_retry_on_permanent_error():
    client = Mock()
    client.request.side_effect = ValueError("Invalid input")
    service = ServiceWithRetry(client, max_retries=3)
    with pytest.raises(ValueError):
        service.fetch()
    assert client.request.call_count == 1  # No retry
```

### Pattern 6: Mocking Time with Freezegun

```python
from freezegun import freeze_time

@freeze_time("2026-01-15 10:00:00")
def test_token_expiry():
    token = create_token(expires_in_seconds=3600)
    assert token.expires_at == datetime(2026, 1, 15, 11, 0, 0)

@freeze_time("2026-01-15 10:00:00")
def test_is_expired_returns_false_before_expiry():
    token = create_token(expires_in_seconds=3600)
    assert not token.is_expired()

@freeze_time("2026-01-15 12:00:00")
def test_is_expired_returns_true_after_expiry():
    token = Token(expires_at=datetime(2026, 1, 15, 11, 30, 0))
    assert token.is_expired()

def test_with_time_travel():
    with freeze_time("2026-01-01") as frozen_time:
        item = create_item()
        assert item.created_at == datetime(2026, 1, 1)
        frozen_time.move_to("2026-01-15")
        assert item.age_days == 14
```

### Pattern 7: Test Markers

```python
@pytest.mark.slow
def test_slow_operation(): ...

@pytest.mark.integration
def test_database_integration(): ...

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature(): ...

@pytest.mark.skipif(os.name == "nt", reason="Unix only test")
def test_unix_specific(): ...

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug(): ...

# Run selectively:
# pytest -m slow
# pytest -m "not slow"
# pytest -m integration
```

## Test Design Principles

### One Behavior Per Test

```python
# BAD — testing multiple behaviors
def test_user_service():
    user = service.create_user(data)
    assert user.id is not None
    updated = service.update_user(user.id, {"name": "New"})
    assert updated.name == "New"

# GOOD — focused tests
def test_create_user_assigns_id():
    assert service.create_user(data).id is not None

def test_update_user_changes_name():
    user = service.create_user(data)
    assert service.update_user(user.id, {"name": "New"}).name == "New"
```

### Always Test Error Paths

```python
def test_get_user_raises_not_found():
    with pytest.raises(UserNotFoundError) as exc_info:
        service.get_user("nonexistent-id")
    assert "nonexistent-id" in str(exc_info.value)
```

## Test Organization

```
tests/
  conftest.py           # Shared fixtures
  test_unit/            # Unit tests
    test_models.py
    test_utils.py
  test_integration/     # Integration tests
    test_api.py
    test_database.py
  test_e2e/             # End-to-end tests
    test_workflows.py
```

## Test Naming Convention

A common pattern: `test_<unit>_<scenario>_<expected_outcome>`. Adapt to your team's preferences.

```python
# Pattern: test_<unit>_<scenario>_<expected>
def test_create_user_with_valid_data_returns_user():
    ...

def test_create_user_with_duplicate_email_raises_conflict():
    ...

def test_get_user_with_unknown_id_returns_none():
    ...
```

## Coverage Reporting

```bash
pip install pytest-cov
pytest --cov=myapp tests/
pytest --cov=myapp --cov-report=html tests/
pytest --cov=myapp --cov-fail-under=80 tests/
pytest --cov=myapp --cov-report=term-missing tests/
```
