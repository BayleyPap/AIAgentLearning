import json
from datetime import datetime, timezone
from pathlib import Path

INPUT_PATH = Path("input.json")
OUTPUT_PATH = Path("output.json")


def read(input_path: Path) -> list:
    try:
        data = json.loads(input_path.read_text())
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Input file is not valid JSON: {e}")


def add_timestamp(data: list) -> list:
    now = datetime.now(timezone.utc).isoformat()
    for entry in data:
        entry["timestamp"] = now
    return data


def filter_by_records(data: list, filter_value: int) -> list:
    return [entry for entry in data if entry["value"] >= filter_value]


def write(data: list, output_path: Path) -> None:
    try:
        output_path.write_text(json.dumps(data, indent=2))
    except TypeError:
        raise TypeError("Data cannot be serialized")
    except FileNotFoundError:
        raise FileNotFoundError(f"Parent directory doesn't exist: {output_path}")


def summary(before: list, after: list) -> dict:
    return {
        "total_input": len(before),
        "total_output": len(after),
        "filtered_out": len(before) - len(after),
    }


def main():
    data = read(INPUT_PATH)
    data = add_timestamp(data)
    data_filtered = filter_by_records(data, 10)
    write(data_filtered, OUTPUT_PATH)
    print(str(summary(data, data_filtered)))


if __name__ == "__main__":
    main()
