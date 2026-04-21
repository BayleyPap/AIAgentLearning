# Async GitHub Client

## What It Does

A CLI tool that takes a GitHub username as an argument and prints the user's profile and recent repos. It fetches the data twice, once synchronously using `requests`, once concurrently using `httpx` and `asyncio`, then prints a timing comparison between the two approaches.

## Why I Built It

This is the Phase 2 refactor of my Phase 1 GitHub client. The original was a single-file script making sequential requests with a hardcoded username. This version introduces concurrent HTTP calls via `asyncio.gather`, takes the username as a CLI argument, and cleans up the architecture so functions are reusable across both sync and async call paths. It also adds proper type hints and a test suite covering the async code path.

## How to Run It

```fish
python -m venv venv
source venv/bin/activate.fish
pip install httpx requests pytest pytest-mock pytest-asyncio
python github_client.py your_github_username_here
```

To run the tests:

```fish
pytest -v
```

### Example output

```fish
venv ❯ python github_client.py BayleyPap
=====Bayley Papworth(BayleyPap)=====
AI Agent Engineer in training | Self-hosted LLMs | Python · LangChain · Docker
Followers: 0
Public repo count: 2
Last pushes:
AIAgentLearning - 2026-04-15T05:07:24Z
BayleyPap - 2026-04-12T01:08:30Z
Sync: 0.776s
=====Bayley Papworth(BayleyPap)=====
AI Agent Engineer in training | Self-hosted LLMs | Python · LangChain · Docker
Followers: 0
Public repo count: 2
Last pushes:
AIAgentLearning - 2026-04-15T05:07:24Z
BayleyPap - 2026-04-12T01:08:30Z
Async: 0.163s
Speedup: 4.75x
```

## What I Learned

Handling missing keys with `.get()` made sense, but I initially failed to consider the case where the key is present with a null value. Using `or` to fall through to a default handles both cases elegantly in a single expression.

Passing a single `httpx.AsyncClient` into both API calls rather than creating one per call avoids repeating the full connection setup on every request. The client maintains a connection pool, so the first request pays the DNS, TCP, and TLS setup cost and subsequent requests to the same host reuse that connection. Without this, concurrent requests still parallelise the waiting but pay the handshake cost twice.

Separating fetching from formatting let me reuse `print_summary` across both the sync and async call paths. The orchestration moved up to `main()` where it belongs, and the presentation layer stopped caring where the data came from. A small architectural change that made the refactor much cleaner.

## What I Would Do Differently

Keeping sync and async implementations of the same logic in one module makes the file longer than it needs to be and blurs the architectural boundary between the two concurrency models. Splitting them into separate modules with a dedicated benchmark script would be cleaner.

Error handling could be improved by raising custom exceptions that the orchestrator catches, rather than returning error dicts. The current pattern forces every caller to check the return type before using the result, which is exactly the kind of clunky contract that Pydantic solves cleanly.

The timing comparison isn't a fair benchmark. The first run (sync) pays all the DNS, TCP, and TLS setup costs, and the second run (async) reuses the cached connections. This inflates the apparent async speedup. A proper benchmark would warm up the connection first, or run each version in isolation.
