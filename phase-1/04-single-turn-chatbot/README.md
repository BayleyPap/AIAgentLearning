# Program 4 — Single-Turn Chatbot

## What It Does
A CLI chatbot that takes user input, sends it to the Anthropic API, and prints
the response. Includes input validation (2–2000 characters), a quit handler,
token usage output after each response, and a Homer Simpson system prompt.

## Why I Built It
To get hands-on experience calling an LLM API directly. No frameworks, no
abstractions, just raw HTTP and response parsing.

## How to Run It
```bash
cd phase-1/04-single-turn-chatbot
python -m venv venv
source venv/bin/activate.fish
pip install anthropic python-dotenv
cp .env.example .env  # add your ANTHROPIC_API_KEY
python chatbot.py
```

## What I Learned
MagicMock is powerful but fails silently. `assert_called_once()` passes without
error because calling any attribute on a MagicMock just returns another
MagicMock. Typos in assertion method names will haunt you.

I also refactored mid-build to extract `send_message()` as a standalone
function so it could accept a client argument directly. Made the tests
significantly cleaner and taught me that testability is an architectural
decision, not an afterthought.

## What I Would Do Differently
Token tracking lives inside `send_message()` which means it prints on every
response whether you want it or not. Should be a separate function triggered
by a user command rather than automatic output.