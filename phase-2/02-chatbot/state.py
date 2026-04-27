import json
from pathlib import Path


class State:
    def __init__(self):
        self.history = []

    def add_turn(self, query: dict, response: dict) -> None:
        self.history.append(query)
        self.history.append(response)

    def __len__(self):
        return len(self.history) // 2

    def clear_history(self) -> int:
        history_len = len(self)
        self.history.clear()
        return history_len

    def get_history(self) -> list[dict]:
        return list(self.history)

    def import_history(self, import_path: Path) -> None:
        try:
            data = json.loads(import_path.read_text())
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {import_path}") from None
        except json.JSONDecodeError as e:
            raise ValueError(f"Input file is not valid JSON: {e}") from e
        if not isinstance(data, list):
            raise TypeError("Input file is not a list")
        self.history = data

    def export_history(self, export_path: Path) -> None:
        try:
            export_path.write_text(json.dumps(self.history, indent=2))
        except TypeError:
            raise TypeError("Data cannot be serialized")
        except FileNotFoundError:
            raise FileNotFoundError(f"Parent directory doesn't exist: {export_path}")

    def get_summary(self) -> str:
        total_chars = sum(len(msg["content"]) for msg in self.history)
        return f"Conversation ended. {len(self)} turns, {total_chars:,} characters exchanged."
