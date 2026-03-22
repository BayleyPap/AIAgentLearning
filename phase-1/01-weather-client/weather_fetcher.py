from datetime import datetime, timedelta, timezone

import requests


def fetch_from_API():
    responce = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=-37.8136&longitude=144.9631&hourly=temperature_2m"
    )
    return responce.json()


def get_current_temp(data: dict) -> float:
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    closest_index = 0
    smallest_diff = float("inf")

    for i, time_str in enumerate(times):
        t = datetime.fromisoformat(time_str)
        diff = abs((t - now).total_seconds())
        if diff < smallest_diff:
            smallest_diff = diff
            closest_index = i
    return temps[closest_index]


def get_tomorrow_temp(data: dict):
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    tomorrow_temps = []

    for i, time_str in enumerate(times):
        if datetime.fromisoformat(time_str).date() == tomorrow:
            tomorrow_temps.append(temps[i])

    return tomorrow_temps


def get_highs_and_lows(data: list):
    tomorrow_temps = get_tomorrow_temp(data)
    return max(tomorrow_temps), min(tomorrow_temps)


def print_weather():
    data = fetch_from_API()
    units = data["hourly_units"]["temperature_2m"]

    current = get_current_temp(data)
    high, low = get_highs_and_lows(data)
    print(f"Current temperature: {current}{units}")

    print(f"Tomorrow will have a high of {high}{units} and a low of {low}{units}")
    print(
        f"Currently {current}{units} in Melbourne — tomorrow expect a high of {high}{units} and a low of {low}{units}."
    )


print_weather()
