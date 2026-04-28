import logging
from pathlib import Path

from anthropic import APIConnectionError, APIStatusError, RateLimitError

from api import API
from cli import formatted_print, get_input, print_help, print_welcome, validate_input
from state import State


def main() -> None:
    api = API()
    state = State()
    print_welcome()
    logging.basicConfig(level=logging.INFO)

    while True:
        try:
            user_input = get_input()
        except KeyboardInterrupt:
            formatted_print(state.get_summary())
            formatted_print("Goodbye!")
            break
        if not validate_input(user_input):
            continue
        if user_input.lower() == "/quit":
            formatted_print(state.get_summary())
            formatted_print("Goodbye!")
            break
        if user_input.lower() == "/clear":
            formatted_print(
                f"Conversation cleared. {state.clear_history()} turns removed."
            )
            continue
        if user_input.lower() == "/help":
            print_help()
            continue
        if user_input.lower().startswith("/save"):
            parts = user_input.split()
            if len(parts) <= 1:
                formatted_print("Usage: /save <filename>")
                continue
            try:
                state.export_history(Path(parts[1]).with_suffix(".json"))
                formatted_print(f"Saved to {parts[1]}")
            except (TypeError, FileNotFoundError) as e:
                formatted_print(f"Save failed: {e}")
            continue
        if user_input.lower().startswith("/load"):
            parts = user_input.split()
            if len(parts) <= 1:
                formatted_print("Usage: /load <filename>")
                continue
            try:
                state.import_history(Path(parts[1]).with_suffix(".json"))
                formatted_print(f"Loaded {len(state)} turns from {parts[1]}.json")
            except (FileNotFoundError, ValueError, TypeError) as e:
                formatted_print(f"Load failed: {e}")
            continue
        if user_input.startswith("/"):
            formatted_print("Command not recognized")
            continue

        query = {"role": "user", "content": user_input}
        try:
            response = api.query_anthropic(state.get_history() + [query])
        except (APIConnectionError,):
            formatted_print(
                "Issue connecting to anthropic please check your network config"
            )
            continue
        except (RateLimitError, APIStatusError):
            formatted_print(
                "Anthropic API is currently experiencing issues please try again later"
            )
            continue
        formatted_print(response)
        state.add_turn(query, {"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
