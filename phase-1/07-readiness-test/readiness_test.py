import re

from anthropic import Anthropic, APIConnectionError, APIStatusError, RateLimitError
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError


class LLMResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)


def setup():
    load_dotenv()
    client = Anthropic()
    return client


def send_msg(history, client):
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            system="respond only in json with the following fields: answer,confidence",
            messages=history,
            max_tokens=1024,
        )
        return response.content[0].text
    except APIConnectionError:
        print("APIConnectionError")
        return None
    except RateLimitError:
        print("Rate limit reached please try again later")
        return None
    except APIStatusError as e:
        print(e.status_code, e.message)
        return None


def get_input() -> str:
    user_input = input(">")
    return user_input.strip()


def extract_json(text: str) -> str:
    return re.sub(r"```json\s*|\s*```", "", text).strip()


def main():
    client = setup()
    history = []

    while True:
        user_input = get_input()
        if user_input.lower() == "quit":
            turn_count = len(history) // 2
            total_chars = sum(len(m["content"]) for m in history)
            print(f"Turns: {turn_count} | Characters exchanged: {total_chars}")
            break
        if len(user_input) < 1:
            print("Input too short")
            continue
        history.append({"role": "user", "content": user_input})
        raw_response = send_msg(history, client)
        if raw_response is None:
            history.pop()
            continue
        extracted_response = extract_json(raw_response)
        try:
            my_llm_response = LLMResponse.model_validate_json(extracted_response)
        except ValidationError as e:
            print(f"Validation failed: {e}")
            history.pop()
            continue
        print(my_llm_response.model_dump_json(indent=2))

        history.append({"role": "assistant", "content": raw_response})


main()
