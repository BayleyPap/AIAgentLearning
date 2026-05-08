import logging

import anthropic
from dotenv import load_dotenv

from config import MAX_TOKENS, MODEL


class API:
    def __init__(self):
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.logger = logging.getLogger(__name__)
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def query_anthropic(self, user_input: str, system_prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": user_input}],
            )
            self.logger.info(
                f"Tokens — input: {response.usage.input_tokens}, output: {response.usage.output_tokens}"
            )
            self.total_input_tokens += response.usage.input_tokens
            self.total_output_tokens += response.usage.output_tokens
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

    def get_token_counts(self) -> tuple[int, int]:
        return self.total_input_tokens, self.total_output_tokens
