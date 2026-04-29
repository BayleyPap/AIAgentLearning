import logging
from pathlib import Path

from anthropic import APIConnectionError, APIStatusError, RateLimitError

from api import API
from cli import formatted_print, get_input, print_help, print_welcome, validate_input
from state import State


def quit_program(state: State, api: API) -> None:
    formatted_print(state.get_summary())
    input_tokens, output_tokens = api.get_token_counts()
    formatted_print(f"Total tokens -- input: {input_tokens}, output: {output_tokens}")
    formatted_print("Goodbye!")


def main() -> None:
    api = API()
    state = State()
    print_welcome()
    logging.basicConfig(level=logging.INFO)

    while True:
        try:
            user_input = get_input()
        except KeyboardInterrupt:
            quit_program(state, api)
            break
        if not validate_input(user_input):
            continue
        if user_input.lower() == "/quit":
            quit_program(state, api)
            break
        if user_input.lower() == "/clear":
            formatted_print(
                f"Conversation cleared. {state.clear_history()} turns removed."
            )
            continue
        if user_input.lower() == "/help":
            print_help()
            continue
        if user_input.lower() == "/history":
            formatted_print(state.get_history_formatted())
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
