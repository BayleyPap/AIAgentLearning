# Experiment 2: Output Format Enforcement

Tested whether system prompts can reliably produce specific output formats across 4 formats and 3 questions per format (12 total responses) using claude-haiku-4-5. Validation automated via the harness.

## System Prompts

**JSON with schema:**
> Respond ONLY with valid JSON matching this schema and nothing else. No preamble, no markdown code fences. Schema: `{"name": "string", "summary": "string", "tags": ["string"]}`

**Markdown table with fixed columns:**
> Respond with a markdown table only. Columns must be exactly: Tool, Use Case, Pros, Cons. No text before or after the table.

**Numbered list, exactly 5 items:**
> Respond with exactly 5 items, numbered 1 to 5. No introduction, no conclusion, no extra items.

**Specific word count (50 words):**
> Respond in exactly 50 words. Not 49, not 51. Count carefully before responding.

## Results

### JSON with schema

| Q | Passed |
|---|---|
| Q1 Linux | PASS |
| Q2 Python | PASS |
| Q3 Docker | PASS |

### Markdown table

| Q | Passed |
|---|---|
| Q1 Linux distros | PASS |
| Q2 Python web frameworks | PASS |
| Q3 Version control systems | PASS |

### Numbered list, exactly 5

| Q | Passed |
|---|---|
| Q1 Database considerations | PASS |
| Q2 Python performance | PASS |
| Q3 Bad codebase signs | PASS |

### Word count, exactly 50

| Q | Passed | Actual count |
|---|---|---|
| Q1 What is an API | FAIL | |
| Q2 Describe Docker | FAIL | |
| Q3 SQL vs NoSQL | FAIL | |

## Analysis

Three of four formats hit 100% pass rate, with word count being the sole failure mode. This suggests output format compliance breaks along a clear line: structural constraints hold reliably, counting constraints do not.

The model can confidently produce a markdown table with the required columns, a numbered list with the right number of items, and JSON with the right schema. These are pattern-matching tasks where the model knows what the shape looks like and produces it. Counting words, by contrast, requires the model to perform an implicit task (tokenise its planned output, count tokens, adjust) that it has no reliable mechanism for. Asking for "exactly 50 words" is asking for behaviour the model genuinely cannot perform consistently.

The JSON results passed validation but every single response was wrapped in markdown code fences, despite the system prompt explicitly forbidding them. The validator silently stripped the fences before parsing, which is why all three passed. This is the practically important takeaway for Phase 4. When using LLM JSON output as Pydantic input, the parser must always strip code fences first. The model treats "no code fences" as a soft suggestion, not a constraint. Assume fences will appear and handle them at the parsing layer rather than relying on prompt instructions to prevent them.
