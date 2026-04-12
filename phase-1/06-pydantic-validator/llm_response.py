import json
import re

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError


class llm_response(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources_needed: bool


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


def send_message(client, prompt: str) -> str:
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system='respond only in JSON matching {"answer": str, "confidence": float 0–1, "sources_needed": bool}',
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except anthropic.APIConnectionError:
        print("Connection failed. Check your network.")
        return None
    except anthropic.RateLimitError:
        print("Rate limit error please try again later")
        return None
    except anthropic.APIStatusError as e:
        print(f"API error {e.status_code}: {e.message}")
        return None


def extract_and_validate_json(text: str) -> dict:
    text = re.sub(r"```json\s*|\s*```", "", text).strip()
    try:
        data = json.loads(text)
        response = llm_response.model_validate(data)
        return response
    except json.JSONDecodeError as e:
        print(f"LLM output is not valid JSON: {e}")
        return None
    except ValidationError as e:
        print("LLM output not valid:")
        for err in e.errors():
            print(f"{err['loc']} : {err['msg']}")

        return None


def main():
    client = setup()
    while True:
        prompt = get_input()
        if prompt.lower() == "quit":
            print("Goodbye!")
            break

        raw = send_message(client, prompt)
        if raw is None:
            continue
        result = extract_and_validate_json(raw)
        print(result)


if __name__ == "__main__":
    main()
