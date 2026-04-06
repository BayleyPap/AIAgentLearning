# Program 5 — Multi-Turn Chatbot

## What It Does

A CLI chatbot that maintains a conversation history across turns, sending the
full message history to the Anthropic API on each request so the model retains
context. Supports saving and loading conversation history to JSON files for
persistence across sessions.

Commands:

- `/help` — prints available commands
- `/clear` — empties history and prints how many turns were removed
- `/save <filename>` — saves conversation history to a JSON file
- `/load <filename>` — loads a previously saved conversation into history
- `/quit` — prints session turn count and exits

Also includes input validation (2–2000 characters), token usage output after
each response, and a Homer Simpson system prompt.

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

Save and resume a conversation:

```
/save mysession
/load mysession
```

No file extension needed -- `.json` is appended automatically.

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
reference unchanged. `.clear()` mutates in place. Extracting `clear_history()`
as a standalone function that returns the removed count made this concrete.

`user_input.split()` returns a new list and discards it if you don't assign
the result. Indexing into the original string with `user_input[1]` gives you
the second character, not the second word. Cost me a debugging session.

## What I Would Do Differently

Exception handling for save and load is done at the call site in `main()`.
A dedicated command dispatcher would be cleaner as the command list grows --
`main()` is already longer than I'd like. Premature optimisation for a Phase 1
program, but the right call for anything beyond this.

`save_history()` silently overwrites existing files. A `--force` flag or an
overwrite prompt would be safer in a real tool.

Token tracking still prints on every response whether you want it or not.
Should be behind a `/verbose` toggle.
