# Phase 1 Foundations — JS→Python Exercises & Data Processor

## What It Does

Nine short scripts that close the Python syntax gap before Week 3 adds network and API complexity. Eight target specific syntax differences between JavaScript and Python: loops, arithmetic formatting, conditionals, error handling, while loops with a counter, file I/O, word frequency counting, and list filtering. The ninth (`process.py`) combines every Week 2 concept into a single data pipeline as a dry run for Program 3 (JSON File Transformer).

## Why I Built These

To get Python syntax off the page and into muscle memory. JavaScript concepts are familiar; the friction is purely syntactic. These scripts eliminate that friction before writing programs that call external APIs.

If the data transformation logic in `process.py` is solid, Program 3 is an incremental step rather than a wall.

## Scripts

| Script | What it does |
|---|---|
| `fibonacci.py` | Prints the first 10 Fibonacci numbers using multiple assignment |
| `celsius_converter.py` | Converts four temperatures from Celsius to Fahrenheit |
| `fizzbuzz.py` | Classic FizzBuzz from 1–100 using `if/elif/else` |
| `safe_divide.py` | Divides two user inputs with explicit `ZeroDivisionError` and `ValueError` handling |
| `collatz.py` | Applies the Collatz sequence from a user-supplied starting number |
| `word_count.py` | Returns a `{word: count}` dict using `dict.get()` for clean frequency counting |
| `filter_evens.py` | Filters even numbers from a list using a list comprehension |
| `file_writer.py` | Writes a list of strings to a `.txt` file using `pathlib.Path` |
| `process.py` | Filters, sorts, and groups student records; writes result to `output.json`; prints a terminal summary |

## How to Run

No virtual environment or pip installs needed — standard library only.

```fish
cd phase-1/00-js-to-python
python fibonacci.py
python celsius_converter.py
python fizzbuzz.py
python safe_divide.py
python collatz.py
python word_count.py
python filter_evens.py
python file_writer.py
python process.py
```

Running `process.py` prints a terminal summary and writes `output.json` to the same directory. `output.json` is excluded from version control — run the script to generate it.

## What I Learned

`:.1f` formats a float to a fixed number of decimal places, which also avoids floating point precision noise in the output (e.g. `32.00000000000001` becoming `32.0`).

`//` performs floor division, returning an integer result rather than a float.

`sorted()` vs `.sort()`: `.sort()` modifies a list in place and returns `None`. Writing `result = my_list.sort()` silently loses your data with no error. `sorted()` returns a new sorted list and leaves the original untouched.

`key=lambda` for sorting dicts: `sorted(students, key=lambda s: s["score"], reverse=True)` tells `sorted()` to compare by the `score` value rather than the whole dict.

`dict.get(key, default)`: used in `word_count.py` to count word frequencies without needing an `if key in dict` check before every increment.

`pathlib` over `open()`: `Path("output.json").write_text(json.dumps(data, indent=2))` is cleaner and more consistent than the `open()/write()/close()` pattern. `json.dumps()` (returns a string) pairs with `write_text()`; `json.dump()` (writes to a file object) pairs with `open()`. Since the roadmap uses `pathlib` everywhere, `json.dumps()` is always the right pairing.

## What I Would Do Differently

`collatz.py` has no input validation for negative numbers or zero. Both cause the sequence to never terminate, resulting in an infinite loop. A guard clause at the top would fix this.

In `process.py`, the grouping step should iterate over the sorted list rather than the unsorted filtered list, so the within-subject ordering by score is preserved in `output.json`. Using one consistent list for both operations removes the ambiguity.
