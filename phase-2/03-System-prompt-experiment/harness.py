import argparse
import json
import re
from pathlib import Path

from anthropic import APIConnectionError, APIStatusError, RateLimitError

from api import API
from config import (
    FORMAT_EXPERIMENTS,
    HELPDESK_PROMPT,
    HELPDESK_PROMPT_B,
    QUESTIONS,
    SYSTEM_PROMPTS,
)


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


def run_personas(api: API, output_dir: Path):
    """Experiment 1: each persona prompt against the shared question set."""
    for persona in SYSTEM_PROMPTS:
        result = []
        for question in QUESTIONS:
            try:
                answer = api.query_anthropic(question, persona["system"])
                result.append({"question": question, "answer": answer})
                print(f"[{persona['name']}] {question[:40]}... -> done")
            except APIConnectionError:
                result.append({"question": question, "error": "connection_error"})
            except (RateLimitError, APIStatusError):
                result.append({"question": question, "error": "api_error"})
        write_to_file(result, output_dir / f"{persona['name']}.json")


def run_formats(api: API, output_dir: Path):
    """Experiment 2: each format experiment with its own questions and validator."""
    for experiment in FORMAT_EXPERIMENTS:
        result = []
        validator = VALIDATORS[experiment["name"]]
        for question in experiment["questions"]:
            try:
                answer = api.query_anthropic(question, experiment["system"])
                passed = validator(answer)
                result.append(
                    {"question": question, "answer": answer, "passed": passed}
                )
                print(
                    f"[{experiment['name']}] {question[:40]}... -> {'PASS' if passed else 'FAIL'}"
                )
            except APIConnectionError:
                result.append({"question": question, "error": "connection_error"})
            except (RateLimitError, APIStatusError):
                result.append({"question": question, "error": "api_error"})
        write_to_file(result, output_dir / f"{experiment['name']}.json")


def run_helpdesk(
    api: API,
    output_dir: Path,
    runs: int = 2,
    prompt: str = HELPDESK_PROMPT,
    label: str = "helpdesk",
):
    """Experiment 3: help desk persona against the scenario set, repeated for variance."""
    scenarios = json.loads(Path("scenarios.json").read_text())

    for run in range(1, runs + 1):
        result = []
        for scenario in scenarios:
            record = {
                "id": scenario["id"],
                "expected_type": scenario["expected_type"],
                "user_message": scenario["user_message"],
                "run": run,
            }
            try:
                record["answer"] = api.query_anthropic(scenario["user_message"], prompt)
                print(f"[{label} run {run}] scenario {scenario['id']} -> done")
            except APIConnectionError:
                record["error"] = "connection_error"
            except (RateLimitError, APIStatusError):
                record["error"] = "api_error"
            result.append(record)
        write_to_file(result, output_dir / f"{label}_run{run}.json")


def main():
    parser = argparse.ArgumentParser(
        description="Run system prompt experiments against the Anthropic API."
    )
    parser.add_argument(
        "experiment",
        choices=["personas", "formats", "helpdesk"],
        help=(
            "Which experiment to run: personas (Experiment 1), "
            "formats (Experiment 2) or helpdesk (Experiment 3)."
        ),
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=2,
        help="Number of repeat runs (helpdesk experiment only).",
    )
    parser.add_argument(
        "--variant",
        choices=["a", "b"],
        default="a",
        help="Help desk prompt variant: a (baseline) or b (single-turn bound).",
    )
    args = parser.parse_args()

    api = API()
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if args.experiment == "personas":
        run_personas(api, output_dir)
    elif args.experiment == "formats":
        run_formats(api, output_dir)
    elif args.experiment == "helpdesk":
        variants = {
            "a": (HELPDESK_PROMPT, "helpdesk"),
            "b": (HELPDESK_PROMPT_B, "helpdesk_b"),
        }
        prompt, label = variants[args.variant]
        run_helpdesk(api, output_dir, args.runs, prompt, label)


if __name__ == "__main__":
    main()
