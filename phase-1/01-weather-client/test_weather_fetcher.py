from datetime import datetime, timedelta, timezone

import pytest
import requests

from weather_fetcher import (
    fetch_from_API,
    get_current_temp,
    get_highs_and_lows,
    get_tomorrow_temp,
)

KNOWN_NOW = datetime(2026, 3, 23, 12, 10, tzinfo=timezone.utc)


@pytest.fixture
def mock_api_responce():
    today = KNOWN_NOW.date()
    tomorrow = (KNOWN_NOW + timedelta(days=1)).date()

    return {
        "hourly_units": {"temperature_2m": "°C"},
        "hourly": {
            "time": [
                f"{today}T12:00",
                f"{today}T13:00",
                f"{tomorrow}T12:00",
                f"{tomorrow}T13:00",
                f"{tomorrow}T14:00",
            ],
            "temperature_2m": [20.0, 21.0, 25.0, 28.0, 22.0],
        },
    }


# How do we test our data if we use current time when we mock the api!?
def test_get_current_temp(mock_api_responce):
    result = get_current_temp(mock_api_responce, now=KNOWN_NOW.replace(tzinfo=None))
    assert result == 20.0


def test_get_tomorrow_temp(mock_api_responce):
    result = get_tomorrow_temp(mock_api_responce, now=KNOWN_NOW.replace(tzinfo=None))
    assert result == [25.0, 28.0, 22.0]


def test_highs_and_lows(mock_api_responce):
    resulta, resultb = get_highs_and_lows(
        mock_api_responce, now=KNOWN_NOW.replace(tzinfo=None)
    )
    assert resulta == 28.0
    assert resultb == 22.0


def test_summary_contains_tomorrow(mock_api_responce):
    data = mock_api_responce
    now = KNOWN_NOW.replace(tzinfo=None)
    units = data["hourly_units"]["temperature_2m"]
    current = get_current_temp(data, now=now)
    high, low = get_highs_and_lows(data, now=KNOWN_NOW)
    summary = f"Currently {current}{units} in Melbourne — tomorrow expect a high of {high}{units} and a low of {low}{units}."
    assert "tomorrow" in summary


def test_connection_error(mocker):
    mock_get = mocker.patch("weather_fetcher.requests.get")
    mock_get.side_effect = requests.exceptions.ConnectionError("no network")

    result = fetch_from_API()
    assert result["error"] == "Connection failed"


def test_timeout_error(mocker):
    mock_get = mocker.patch("weather_fetcher.requests.get")
    mock_get.side_effect = requests.exceptions.Timeout("connection timeout")

    result = fetch_from_API()
    assert result["error"] == "Connection timeout"


def test_http_error(mocker):
    mock_get = mocker.patch("weather_fetcher.requests.get")
    mock_get.side_effect = requests.exceptions.HTTPError("404 file not found")

    result = fetch_from_API()
    assert result["error"] == "HTTP error: 404 file not found"


def test_missing_key_error(mocker):
    mock_get = mocker.patch("weather_fetcher.requests.get")
    mock_get.return_value.json.return_value = {"wrong_key": "wrong_value"}
    mock_get.return_value.raise_for_status.return_value = None

    result = fetch_from_API()

    assert "error" in result
    assert "missing key" in result["error"]
