# Data Processor

## What It Does

Processes a hardcoded list of 8 student records. Filters students who scored 60 or above, sorts them by score from highest to lowest, groups them by subject, and writes the result to `output.json`. Prints a summary to the terminal showing total students, passing count, and the top scorer.

## Why I Built It

Dry run for Program 3 (JSON File Transformer) in Week 3. The goal was to combine every concept from Week 2 — lists, dicts, list comprehensions, `json`, and `pathlib` — into a single working pipeline before adding network complexity. If the data transformation logic is solid here, Program 3 is an incremental step rather than a wall.

## How to Run It

No virtual environment or pip installs needed — standard library only.

```fish
python process.py
```

Running the script prints a terminal summary and writes `output.json` to the same directory. `output.json` is excluded from version control — run the script to generate it.

## What I Learned

- **`sorted()` vs `.sort()`**: `.sort()` modifies a list in place and returns `None`. Writing `result = my_list.sort()` silently loses your data with no error. `sorted()` returns a new sorted list and leaves the original untouched — always the safer default.
- **`key=lambda` for sorting dicts**: `sorted(students, key=lambda s: s["score"], reverse=True)` tells `sorted()` to compare by the `score` value rather than the whole dict. The lambda is just a one-line function that extracts the comparison value.
- **`dict.get(key, default)`**: Used in `word_count.py` to count word frequencies cleanly — `counts.get(word, 0) + 1` avoids needing an `if key in dict` check before every increment.
- **`pathlib` over `open()`**: `Path("output.json").write_text(json.dumps(data, indent=2))` is cleaner and more consistent than the `open()/write()/close()` pattern. `json.dumps()` (returns a string) pairs with `write_text()`; `json.dump()` (writes to a file object) pairs with `open()` — since the roadmap uses `pathlib` everywhere, `json.dumps()` is always the right call.

## What I Would Do Differently

The grouping logic initially iterated over `student_records` (all 8 students) instead of `passing_student_sorted` (the filtered, sorted list). The result was that failing students appeared in `output.json` — a logic bug with no error message, just wrong output. In future I'd be more deliberate about which list each loop operates on, and check the output file manually before considering a step done.
