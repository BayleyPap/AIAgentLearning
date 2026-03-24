# Weather Client

## What It Does

Fetches live weather data for Melbourne from the Open-Meteo API and prints
three things: the current temperature, tomorrow's forecast high and low, and
a one-sentence plain-English summary. No API key required — Open-Meteo is
free and open.

## Why I Built It

Program 1 of the Phase 1 Python Foundation roadmap. The goal was to build
a working HTTP client that parses a real JSON response, extracts meaningful
data from a nested structure, and handles failure cases cleanly — without
relying on any abstractions beyond the standard library and `requests`.

## How to Run It

```fish
# Clone the repo and navigate to this folder
cd phase-1/01-weather-client

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate.fish

# Install dependencies
pip install requests pytest pytest-mock

# Run the program
python weather_fetcher.py

# Run the tests
pytest -v
```

Expected output:
```
Current temperature: 21.4°C
Tomorrow will have a high of 25.3°C and a low of 19.3°C
Currently 21.4°C in Melbourne — tomorrow expect a high of 25.3°C and a low of 19.3°C.
```

## What I Learned

**Parallel list structures in API responses.** The Open-Meteo API returns
`time` and `temperature_2m` as two separate lists at matching indexes. Once
I understood that structure, finding the current temperature became an index
lookup problem rather than a search problem.

**Dependency injection for testability.** `get_current_temp()` and
`get_tomorrow_temp()` both originally called `datetime.now()` internally,
which made them non-deterministic in tests — the correct answer would change
depending on when you ran the test. Refactoring to accept `now` as an
optional parameter with `None` as the default fixed this cleanly. Production
behaviour is unchanged; tests pass a known constant instead.

**The patch path is the import path, not the source path.** When mocking
`requests.get` in tests, the correct patch target is
`weather_fetcher.requests.get` — where the name lives in the module being
tested — not `requests.get` where it originates. Getting this wrong means
the real API gets called during tests.

**`_` as a throwaway variable.** Using `_ = data["hourly"]["time"]` to
validate key existence without needing the value is a Python convention that
signals intent clearly — the point is the potential `KeyError`, not the data
itself.

## What I Would Do Differently

**Timezone handling.** The API returns times in GMT and I'm in Melbourne
(AEDT, UTC+11). The current implementation compares GMT times to GMT now,
which is consistent — but "tomorrow" in GMT and "tomorrow" in Melbourne are
different things late at night. A production version would convert API times
to local timezone before any date comparisons.

**Separate data fetching from data processing.** `fetch_from_API()` currently
does both the HTTP call and key validation. Splitting these into
`fetch_raw()` and `validate_response()` would make each easier to test in
isolation and easier to swap out if the API changes.

**More granular error messages.** The `KeyError` handler currently returns
the missing key name but doesn't tell the caller which function failed or
what the full response looked like. In a production client that would make
debugging significantly faster.
