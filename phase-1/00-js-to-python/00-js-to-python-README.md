# JS→Python Translation Exercises

## What It Does

Five short scripts that reimplement common programming patterns in Python. Each script targets a specific syntax difference between JavaScript and Python: loops, arithmetic formatting, conditionals, error handling, and while loops with a counter.

## Why I Built It

To get Python syntax off the page and into muscle memory before writing programs that call external APIs. JavaScript concepts are familiar — the friction is purely syntactic. These scripts eliminate that friction.

## Scripts

| Script | What it does |
|---|---|
| `fibonacci.py` | Prints the first 10 Fibonacci numbers using multiple assignment |
| `celsius_converter.py` | Converts four temperatures from Celsius to Fahrenheit |
| `fizzbuzz.py` | Classic FizzBuzz from 1–100 using `if/elif/else` |
| `safe_divide.py` | Divides two user inputs with explicit error handling |
| `collatz.py` | Applies the Collatz sequence from a user-supplied starting number |

## How to Run It

No dependencies. Requires Python 3.11.9 via pyenv.

```fish
cd phase-1/00-js-to-python
python fibonacci.py
python celsius_converter.py
python fizzbuzz.py
python safe_divide.py
python collatz.py
```

## What I Learned
`:.1f` formats a float to a fixed number of decimal places, which also avoids
floating point precision errors in the output (e.g. `32.00000000000001` becoming `32.0`).
`//` performs floor division, returning an integer result rather than a float.

## What I Would Do Differently
Add input validation to `collatz.py` to reject negative numbers and zero —
both cause the sequence to never terminate, resulting in an infinite loop.