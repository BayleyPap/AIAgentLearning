import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv


def setup():
    load_dotenv()
    client = anthropic.Anthropic()
    return client


def get_input() -> str:
    while True:
        print("Please provide your LLM prompt or type '/help' to see list of commands:")
        user_input = input(">").strip()
        if len(user_input) < 2:
            print("Message too short.")
            continue
        if len(user_input) > 2000:
            print(f"Message too long ({len(user_input)} chars). 2000 maximum")
            continue
        return user_input


def send_message(client, history: list) -> str:
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="Respond to every query roleplaying the character of Homer from 'The Simpsons'",
            messages=history,
        )
        print(
            f"Tokens — input: {response.usage.input_tokens}, output: {response.usage.output_tokens}"
        )
        return response.content[0].text
    except anthropic.APIConnectionError:
        return "Connection failed. Check your network."
    except anthropic.RateLimitError:
        return "Rate limit error please try again later"
    except anthropic.APIStatusError as e:
        return f"API error {e.status_code}: {e.message}"


def clear_history(history: list) -> int:
    count = len(history) // 2
    history.clear()
    return count


def save_history(history: list, file_name: str) -> None:
    try:
        Path(file_name + ".json").write_text(json.dumps(history, indent=2))
    except TypeError:
        raise TypeError("Data cannot be serialized")
    except FileNotFoundError:
        raise FileNotFoundError(f"Parent directory doesn't exist: {file_name}")


def load_history(file_name: str) -> list:
    try:
        history = json.loads(Path(file_name + ".json").read_text())
        return history
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {file_name + '.json'}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Input file is not valid JSON: {e}")


def main():
    client = setup()
    history = []

    while True:
        user_input = get_input()
        if user_input.lower() == "/quit":
            print(f"Turn count: {len(history) // 2}")
            print("Goodbye!")
            break
        if user_input.lower() == "/clear":
            print(f"Conversation cleared. {clear_history(history)} turns removed.")
            continue
        if user_input.lower() == "/help":
            print("""
/help - prints this help message
/quit - exits the program
/clear - clears chat history
/save file_name - saves conversation history as a JSON file with the file name specified, don't include file type extension
/load file_name - loads file into conversation history, don't include file type extension""")
            continue
        if user_input.lower().startswith("/save"):
            parts = user_input.split()
            if len(parts) <= 1:
                print("Usage: /save <filename>")
                continue
            try:
                save_history(history, parts[1])
                print(f"Saved to {parts[1]}.json")
            except (TypeError, FileNotFoundError) as e:
                print(f"Save failed: {e}")
            continue
        if user_input.lower().startswith("/load"):
            parts = user_input.split()
            if len(parts) <= 1:
                print("Usage: /load <filename>")
                continue
            try:
                history = load_history(parts[1])
                print(f"Loaded {len(history) // 2} turns from {parts[1]}.json")
            except (FileNotFoundError, ValueError) as e:
                print(f"Load failed: {e}")
            continue
        if user_input.lower()[0] == "/":
            print("Command not recognized")
            continue

        history.append({"role": "user", "content": user_input})
        assistant_response = send_message(client, history)
        history.append({"role": "assistant", "content": assistant_response})
        print(assistant_response)


if __name__ == "__main__":
    main()
