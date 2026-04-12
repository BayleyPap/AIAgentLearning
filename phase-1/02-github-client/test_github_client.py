import requests

from github_client import get_profile, get_repos


def test_repos_sorted_by_push_date(mocker):
    mock_get = mocker.patch("github_client.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.headers = {"X-RateLimit-Remaining": "50"}
    mock_get.return_value.json.return_value = [
        {"name": "old-repo", "pushed_at": "2026-01-01T00:00:00Z"},
        {"name": "newest-repo", "pushed_at": "2026-03-20T00:00:00Z"},
        {"name": "middle-repo", "pushed_at": "2026-02-15T00:00:00Z"},
    ]

    result = get_repos()
    assert result[0]["name"] == "newest-repo"
    assert result[2]["name"] == "old-repo"


def test_fetch_not_found(mocker):
    mock_get = mocker.patch("github_client.requests.get")
    mock_get.return_value.status_code = 404
    mock_get.return_value.headers = {"X-RateLimit-Remaining": "50"}

    result = get_profile()
    assert result["error"] == "User not found"


def test_fetch_rate_limit(mocker):
    mock_get = mocker.patch("github_client.requests.get")
    mock_get.return_value.headers = {"X-RateLimit-Remaining": "0"}

    result = get_profile()
    assert result["error"] == "Rate limit reached. Try again later."


def test_fetch_connection_error(mocker):
    mock_get = mocker.patch("github_client.requests.get")
    mock_get.side_effect = requests.exceptions.ConnectionError("no network")

    result = get_profile()
    assert result["error"] == "Connection failed"
