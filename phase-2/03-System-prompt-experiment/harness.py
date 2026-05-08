import json
import re
from pathlib import Path

from anthropic import APIConnectionError, APIStatusError, RateLimitError

from api import API
from config import FORMAT_EXPERIMENTS


def write_to_file(data: list, path: Path):
    path.write_text(json.dumps(data, indent=2))


def validate_json(text: str) -> bool:
    stripped = re.sub(r"```json\s*|\s*```", "", text).strip()
    try:
        json.loads(stripped)
        return True
    except json.JSONDecodeError:
        return False


def validate_table(text: str) -> bool:
    stripped_text = text.strip()
    if not stripped_text.startswith("|"):
        return False
    if not stripped_text.endswith("|"):
        return False
    lines = stripped_text.split("\n")
    required = ["Tool", "Use Case", "Pros", "Cons"]
    header = lines[0]
    for column in required:
        if column not in header:
            return False
    return True


def validate_numbered_list(text: str) -> bool:
    matches = re.findall(r"^\d+\.", text, re.MULTILINE)
    return len(matches) == 5


def validate_word_count(text: str) -> bool:
    split_text = text.split()
    return len(split_text) == 50


VALIDATORS = {
    "json_schema": validate_json,
    "markdown_table": validate_table,
    "numbered_list_5": validate_numbered_list,
    "word_count_50": validate_word_count,
}


def main():
    api = API()
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    for experiment in FORMAT_EXPERIMENTS:
        result = []
        validator = VALIDATORS[experiment["name"]]

        for question in experiment["questions"]:
            try:
                answer = api.query_anthropic(question, experiment["system"])
                passed = validator(answer)
                result.append(
                    {
                        "question": question,
                        "answer": answer,
                        "passed": passed,
                    }
                )
                print(
                    f"[{experiment['name']}] {question[:40]}... -> {'PASS' if passed else 'FAIL'}"
                )
            except APIConnectionError:
                result.append({"question": question, "error": "connection_error"})
            except (RateLimitError, APIStatusError):
                result.append({"question": question, "error": "api_error"})

        write_to_file(result, output_dir / f"{experiment['name']}.json")


if __name__ == "__main__":
    main()
