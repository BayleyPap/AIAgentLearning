# GitHub Client

## What It Does

Fetches a GitHub user's public profile and repository list via the GitHub REST API. Prints the user's name, bio, follower count, public repo count, and their 3 most recently pushed repositories with push dates.

## Why I Built It

Program 2 of Phase 1 — designed to practise working with a multi-endpoint API, parsing response headers, and handling multiple error cases (rate limiting, connection errors, HTTP errors). First program to separate the HTTP logic into a shared `fetch_api` function reused by both `get_profile` and `get_repos`.

## How to Run It

```fish
cd phase-1/02-github-client
python -m venv venv
source venv/bin/activate.fish
pip install requests pytest pytest-mock
```

Run the client:

```fish
python github_client.py
```

Run the tests:

```fish
pytest -v
```

## What I Learned

The `X-RateLimit-Remaining` header is a string, not an integer — `int(response.headers.get("X-RateLimit-Remaining", 1))` requires the explicit cast or the comparison fails silently.

The rate limit check has to happen before `raise_for_status()` — the header is present on all responses regardless of status code, so checking it early avoids misclassifying a rate-limited response as a generic HTTP error.

Extracting shared HTTP logic into a single `fetch_api` function kept `get_profile` and `get_repos` clean, and meant all four error cases only needed to be handled once.

## What I Would Do Differently

`get_repos` calls `sorted()` directly on the return value of `fetch_api` without checking whether it got back a list or an error dict. If the API call fails, `sorted()` will crash trying to sort a dict. Adding a guard — `if isinstance(repos, dict) and "error" in repos: return repos` — before the sort would make the error handling consistent with `get_profile`.

Would also pull `USERNAME` from a `.env` file via `python-dotenv` rather than hardcoding it, so the client works for any GitHub user without editing the source.
