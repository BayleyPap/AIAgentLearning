# Program 5 — Multi-Turn Chatbot

## What It Does

A CLI chatbot that maintains a conversation history across turns, sending the
full message history to the Anthropic API on each request so the model retains
context. Includes input validation (2–2000 characters), a `clear` command that
empties history and reports how many turns were removed, a `quit` command that
prints the session turn count, token usage output after each response, and a
Homer Simpson system prompt.

## Why I Built It

To build stateful conversation handling on top of a stateless API. The
Anthropic API has no built-in memory -- context is maintained entirely by
accumulating a messages list locally and sending it in full on every call.
This pattern underlies every agent system from Phase 3 onwards.

## How to Run It

```bash
pip install anthropic python-dotenv
cp .env.example .env  # add your ANTHROPIC_API_KEY
python chatbot.py
```

## System Prompt Design

The system prompt instructs the model to roleplay as Homer Simpson from The
Simpsons on every response. Constraints: stay in character at all times, use
Homer's speech patterns and vocabulary, reference donuts and beer naturally,
and never break the fourth wall.

A persona-constrained prompt was chosen over a generic assistant prompt to
make context retention obvious during testing -- if the model forgets your
name mid-conversation, the failure is immediately visible.

## What I Learned

`history = []` vs `history.clear()` is not interchangeable inside functions.
Rebinding with `= []` creates a new local list and leaves the caller's
reference unchanged. `.clear()` mutates in place. This matters the moment you
extract history manipulation into a helper function -- the test for
`clear_history()` would silently pass while the actual list in `main()` stayed
untouched.

The `clear_history()` function returns the turn count before clearing so the
caller can print it without needing to measure the list twice. Small thing but
it keeps the logic in one place.

## What I Would Do Differently

`send_message()` prints token usage on every call. That output belongs behind
a verbose flag or a dedicated `tokens` command rather than always-on noise.
Same issue carried over from Program 4 and still not fixed.

History grows without bound. A production version would cap it or implement a
sliding window to avoid eventually exceeding the model's context limit.
