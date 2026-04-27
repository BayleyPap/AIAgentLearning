import logging

import anthropic
from dotenv import load_dotenv

from config import MAX_TOKENS, MODEL, SYSTEM_PROMPT


class API:
    def __init__(self):
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.logger = logging.getLogger(__name__)

    def query_anthropic(self, messages: list[dict]) -> str:
        try:
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=messages,
            )
            self.logger.info(
                f"Tokens — input: {response.usage.input_tokens}, output: {response.usage.output_tokens}"
            )
            return response.content[0].text
        except anthropic.APIConnectionError as e:
            self.logger.error(f"Connection error: {e}")
            raise
        except anthropic.RateLimitError as e:
            self.logger.error(f"Rate limit error: {e}")
            raise
        except anthropic.APIStatusError as e:
            self.logger.error(f"API error {e.status_code}: {e.message}")
            raise
