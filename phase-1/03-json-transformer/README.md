# JSON File Transformer

## What It Does

Reads a JSON file containing a list of records, adds a UTC timestamp to every record, filters out records where `value < 10`, and writes the result to an output file. Prints a summary of how many records were processed, kept, and filtered.

## Why I Built It

Program 3 of Phase 1 — designed to solidify file I/O with `pathlib`, JSON serialisation, and data transformation with list comprehensions. Also the first program where the test suite covers both happy paths and failure paths (missing file, invalid JSON, missing output directory).

## How to Run It

```fish
cd phase-1/03-json-transformer
python -m venv venv
source venv/bin/activate.fish
pip install pytest
```

Create an `input.json` file in the same directory:

```json
[
  {"id": 1, "name": "Alice", "category": "A", "value": 15},
  {"id": 2, "name": "Bob", "category": "B", "value": 5},
  {"id": 3, "name": "Carol", "category": "A", "value": 20},
  {"id": 4, "name": "Dave", "category": "B", "value": 3},
  {"id": 5, "name": "Eve", "category": "A", "value": 12}
]
```

Run the transformer:

```fish
python transformer.py
```

Run the tests:

```fish
pytest -v
```

## What I Learned

`del entry` inside a `for` loop does nothing — it deletes the local loop variable, not the item from the list. The correct approach for filtering is a list comprehension with the condition flipped: keep records where `value >= 10` rather than trying to delete records where `value < 10`.

Separating file boundary functions (`read`, `write`) from pure data transformation functions (`add_timestamp`, `filter_by_records`, `summary`) made testing significantly cleaner. The transformation functions take and return plain lists, so tests can use a simple data fixture with no file I/O at all. Only the file boundary tests need `tmp_path`.

Calling `datetime.now()` inside a loop gives every record a microsecond-different timestamp. Calling it once before the loop and reusing the value is the correct approach.

## What I Would Do Differently

Accept the filter threshold and file paths as CLI arguments (`sys.argv`) rather than hardcoded constants, so the program is reusable without editing the source. Would also add a check that the input is actually a list before processing — currently passing a JSON object instead of a JSON array would cause a confusing error downstream.
