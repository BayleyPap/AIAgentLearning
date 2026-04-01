import anthropic
from dotenv import load_dotenv


def setup():
    load_dotenv()
    client = anthropic.Anthropic()
    return client


def get_input() -> str:
    while True:
        print("Please provide your LLM prompt or type 'quit' to exit program:")
        user_input = input(">").strip()
        if len(user_input) < 2:
            print("Message too short.")
            continue
        if len(user_input) > 2000:
            print(f"Message too long ({len(user_input)} chars). 2000 maximum")
            continue
        return user_input


def send_message(client, user_input: str) -> str:
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_input}],
        )
        return response.content[0].text
    except anthropic.APIConnectionError:
        return "Connection failed. Check your network."
    except anthropic.RateLimitError:
        return "Rate limit error please try again later"
    except anthropic.APIStatusError as e:
        return f"API error {e.status_code}: {e.message}"


def main():
    client = setup()

    while True:
        user_input = get_input()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        print(send_message(client, user_input))


if __name__ == "__main__":
    main()
