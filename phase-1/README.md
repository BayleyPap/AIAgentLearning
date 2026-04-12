# Phase 1 — Python Foundation

## What This Phase Was

Eight weeks of Python from scratch. I have a CS degree that has been sitting unused for a few years and a JavaScript background, so the concepts were familiar but the syntax was not. The goal was to get to the point where I could build a working Python program that calls an API, parses JSON, and handles errors without looking anything up. That is the bar for Phase 2.

## Stack

Python 3.11.9, requests, anthropic, pydantic v2, python-dotenv, pytest, pytest-mock, pathlib

## Programs

| Program | What It Demonstrates |
|---|---|
| `00-js-to-python/` | Syntax exercises: loops, error handling, file I/O, list comprehensions, data pipelines |
| `01-weather-client/` | HTTP client, nested JSON parsing, dependency injection for testability, mocking external APIs |
| `02-github-client/` | Multi-endpoint API, response header parsing, shared fetch function, rate limit and 404 handling |
| `03-json-transformer/` | File I/O with pathlib, data transformation pipeline, separating pure functions from file boundary functions |
| `04-single-turn-chatbot/` | Anthropic API integration, input validation, structured error handling, mocking the API client in tests |
| `05-multi-turn-chatbot/` | Stateful conversation via accumulated message history, command dispatcher, save/load persistence to JSON |
| `06-pydantic-validator/` | Structured output extraction from an LLM, Pydantic v2 runtime validation, handling API failures separately from validation failures |

## Key Things Learned

The patch path is the import path. Mocking `requests.get` patches the library globally. Mocking `weather_fetcher.requests.get` patches the name as it exists in the module being tested. Getting this wrong means real network calls happen during tests.

`sorted()` returns a new list. `.sort()` sorts in place and returns `None`. Writing `result = my_list.sort()` loses your data silently.

Testability is an architecture decision. `send_message()` in the chatbot originally called `client` from the outer scope. Refactoring to accept `client` as a parameter made it mockable. The design change was one line but it required thinking about the function boundary differently.

`assert_called_once()` with a typo passes silently. Any attribute access on a MagicMock returns another MagicMock, so `mock.assert_called_wonce()` does not raise, it just does nothing. This is one of the more unpleasant pytest-mock gotchas.

Calling `datetime.now()` inside a loop gives every record a different timestamp. Call it once before the loop.

## How to Run Any Program

Each program has its own venv and README with exact setup steps. The general pattern:

```fish
cd phase-1/<program-folder>
python -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt   # or see the program README for deps
pytest -v
python <main_file>.py
```
