# System Prompt Experiments

Two experiments testing how reliably system prompts control model behaviour with `claude-haiku-4-5`, and where that control breaks down. The findings feed directly into Phase 4 agent prompt design.

## The Headline Finding

Both experiments converged on the same principle from different angles: **positive constraints ("always do X") hold reliably; negative constraints ("never do X") leak.** Prohibitions are treated as soft suggestions, and the model interprets every constraint semantically rather than literally, satisfying the letter of a rule while defeating its intent.

## Experiment 1: Persona and Tone Control

Three personas (terse expert, patient teacher, devil's advocate) across 5 questions, scored manually for in-character behaviour and constraint violations. Full write-up: [system_prompt_results.md](output/system_prompt_results.md).

Key result: the Devil's Advocate (a single positive behavioural instruction) held character on all 5. The Terse Expert (a stack of prohibitions) was the least reliable, producing a functionally bulleted list where bullets were forbidden and a five-clause run-on where "one sentence" was required. A default "Great question" opener leaked into the persona that didn't forbid it and never appeared in the one that did.

## Experiment 2: Output Format Enforcement

Four formats (JSON schema, markdown table, numbered list, exact word count) across 3 questions each, validated automatically by the harness. Full write-up: [format_results.md](output/format_results.md).

Key result: structural constraints hit 100%, the counting constraint (exactly 50 words) failed all 3. Structure is a pattern-match the model can produce; counting requires a mechanism it doesn't have. Separately, every JSON response came wrapped in code fences despite the prompt forbidding them: the validator strips fences before parsing, which is the only reason they passed. The Phase 4 takeaway is load-bearing: treat LLM JSON output as always fenced and strip at the parsing layer, never trust the prompt to prevent it.

## Running It

​```bash
python -m venv venv
source venv/bin/activate      # fish: source venv/bin/activate.fish
pip install -r requirements.txt
python harness.py personas    # Experiment 1
python harness.py formats     # Experiment 2
​```

`harness.py` is a shared runner; the experiment is selected by argument. Results are written to `output/` as one JSON file per prompt or format. All prompts and questions live in `config.py`.

Requires an `ANTHROPIC_API_KEY`. Create a `.env` file in this directory containing:

​```
ANTHROPIC_API_KEY=your-key-here
​```

## Files

| File | Purpose |
|---|---|
| `config.py` | System prompts, questions, and format experiment definitions |
| `api.py` | Anthropic client wrapper with token tracking |
| `harness.py` | Runs the selected experiment, validates output, writes results |
| `output/*.md` | The two analysis write-ups (the actual deliverables) |
| `output/*.json` | Raw per-question responses |
