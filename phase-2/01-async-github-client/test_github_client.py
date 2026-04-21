import pytest

from github_client import async_fetch_api, async_fetch_both


@pytest.mark.asyncio
async def test_async_fetch_api_success(mocker):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"X-RateLimit-Remaining": "5000"}
    mock_response.json.return_value = {"login": "bayleypap", "followers": 42}
    mock_response.raise_for_status.return_value = None

    mock_client = mocker.AsyncMock()
    mock_client.get.return_value = mock_response

    result = await async_fetch_api(
        mock_client, "https://api.github.com/users/bayleypap"
    )

    assert result["login"] == "bayleypap"
    mock_client.get.assert_called_once_with(
        "https://api.github.com/users/bayleypap", timeout=5
    )


@pytest.mark.asyncio
async def test_async_fetch_api_rate_limit(mocker):
    """async_fetch_api returns error dict when rate limit hit."""
    mock_response = mocker.MagicMock()
    mock_response.headers = {"X-RateLimit-Remaining": "0"}

    mock_client = mocker.AsyncMock()
    mock_client.get.return_value = mock_response

    result = await async_fetch_api(
        mock_client, "https://api.github.com/users/bayleypap"
    )

    assert "error" in result
    assert "rate limit" in result["error"].lower()


@pytest.mark.asyncio
async def test_async_fetch_both_calls_both_endpoints(mocker):
    """async_fetch_both fetches profile and repos concurrently."""
    # Mock the fetch_api function itself, not httpx
    mock_fetch = mocker.patch("github_client.async_fetch_api")
    mock_fetch.side_effect = [
        {"login": "bayleypap", "followers": 42},  # profile response
        [{"name": "repo1", "pushed_at": "2026-04-01"}],  # repos response
    ]

    profile, repos = await async_fetch_both("bayleypap")

    assert profile["login"] == "bayleypap"
    assert len(repos) == 1
    assert mock_fetch.call_count == 2
