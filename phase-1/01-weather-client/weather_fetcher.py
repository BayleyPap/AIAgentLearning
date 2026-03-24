from datetime import datetime, timedelta, timezone

import requests


def fetch_from_API():
    try:
        responce = requests.get(
            "https://api.open-meteo.com/v1/forecast?latitude=-37.8136&longitude=144.9631&hourly=temperature_2m",
            timeout=5,
        )
        responce.raise_for_status()
        data = responce.json()
        _ = data["hourly"]["time"]
        _ = data["hourly"]["temperature_2m"]
        _ = data["hourly_units"]["temperature_2m"]
        return data
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except requests.exceptions.Timeout:
        return {"error": "Connection timeout"}
    except KeyError as e:
        return {"error": f"Unexpected API response structure, missing key: {e}"}


def get_current_temp(data: dict, now: datetime = None) -> float:
    if now is None:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
    else:
        now = now.replace(tzinfo=None)

    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    closest_index = 0
    smallest_diff = float("inf")

    for i, time_str in enumerate(times):
        t = datetime.fromisoformat(time_str)
        diff = abs((t - now).total_seconds())
        if diff < smallest_diff:
            smallest_diff = diff
            closest_index = i
    return temps[closest_index]


def get_tomorrow_temp(data: dict, now: datetime = None) -> list[float]:
    if now is None:
        now = datetime.now(timezone.utc)

    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    tomorrow_temps = []

    for i, time_str in enumerate(times):
        if datetime.fromisoformat(time_str).date() == tomorrow:
            tomorrow_temps.append(temps[i])

    return tomorrow_temps


def get_highs_and_lows(data: dict, now: datetime = None):
    tomorrow_temps = get_tomorrow_temp(data, now=now)
    return max(tomorrow_temps), min(tomorrow_temps)


def print_weather():
    data = fetch_from_API()
    now = datetime.now(timezone.utc)
    units = data["hourly_units"]["temperature_2m"]

    current = get_current_temp(data, now=now)
    high, low = get_highs_and_lows(data, now=now)
    print(f"Current temperature: {current}{units}")

    print(f"Tomorrow will have a high of {high}{units} and a low of {low}{units}")
    print(
        f"Currently {current}{units} in Melbourne — tomorrow expect a high of {high}{units} and a low of {low}{units}."
    )


if __name__ == "__main__":
    print_weather()
