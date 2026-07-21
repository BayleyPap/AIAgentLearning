# System Prompt Experiments

Three experiments testing how reliably system prompts control model behaviour with `claude-haiku-4-5`, and where that control breaks down. The findings feed directly into Phase 3 evaluation design and Phase 4 agent prompt design.

## The Headline Finding

All three experiments converged on the same principle from different angles: **the model satisfies the visible shape of a constraint and defeats its intent.** A rule that describes a form the model can pattern-match holds near-perfectly. A rule that requires the model to assess its own limits, count, or decide when to stop, gets satisfied in appearance and abandoned in substance. Related, and confirmed twice: positive constraints ("always do X") hold better than prohibitions ("never do X"), which are treated as soft suggestions.

Experiment 3 added one finding the first two could not reach: pressure to comply with a constraint can produce fabrication. Forced to commit to an answer, the model invented plausible causes for an error code it had no way to interpret, on the one scenario where the prompt explicitly told it to escalate instead.

## Experiment 1: Persona and Tone Control

Three personas (terse expert, patient teacher, devil's advocate) across 5 questions, scored manually for in-character behaviour and constraint violations. Full write-up: [system_prompt_results.md](output/system_prompt_results.md).

Key result: the Devil's Advocate (a single positive behavioural instruction) held character on all 5. The Terse Expert (a stack of prohibitions) was the least reliable, producing a functionally bulleted list where bullets were forbidden and a five-clause run-on where "one sentence" was required. A default "Great question" opener leaked into the persona that didn't forbid it and never appeared in the one that did.

## Experiment 2: Output Format Enforcement

Four formats (JSON schema, markdown table, numbered list, exact word count) across 3 questions each, validated automatically by the harness. Full write-up: [format_results.md](output/format_results.md).

Key result: structural constraints hit 100%, the counting constraint (exactly 50 words) failed all 3. Structure is a pattern-match the model can produce; counting requires a mechanism it doesn't have. Separately, every JSON response came wrapped in code fences despite the prompt forbidding them: the validator strips fences before parsing, which is the only reason they passed. The Phase 4 takeaway is: treat LLM JSON output as always fenced and strip at the parsing layer, never trust the prompt to prevent it.

## Experiment 3: Help Desk Persona and Escalation Behaviour

An IT help desk agent with a defined capability boundary, run against 5 support tickets written in user voice. Two prompt variants, two runs each, 20 responses total. Scored manually on whether the model committed to a decision, whether it fabricated, and whether the decision was right. Full write-up: [helpdesk_results.md](output/helpdesk_results.md).

Key result: the baseline prompt never reached a decision on any of its 10 responses, because "establish the scope of a problem before proposing a fix" is unbounded in a single turn and consumed every response. Variant B added one paragraph binding the model to a single turn, which lifted commitment to 5 of 10. Where it still failed it failed in two ways worth having: several responses printed a Decision heading and then deferred underneath it, and the two responses about an opaque vendor error code invented likely causes rather than escalating as the prompt instructed.

The scenario set lives in `scenarios.json` rather than in `config.py` because it is reused downstream: it seeds the Phase 3 knowledge bot evaluation set and the Phase 5 fine-tuning evaluation set. The fabrication result is why that Phase 3 set carries escalate scenarios and a decline rate metric alongside pass rate.

## Running It

```bash
python -m venv venv
source venv/bin/activate      # fish: source venv/bin/activate.fish
pip install -r requirements.txt
python harness.py personas                  # Experiment 1
python harness.py formats                   # Experiment 2
python harness.py helpdesk                  # Experiment 3, variant A
python harness.py helpdesk --variant b      # Experiment 3, variant B
```

`harness.py` is a shared runner; the experiment is selected by argument. Results are written to `output/` as one JSON file per prompt, format, or run. All prompts and questions live in `config.py`.

The help desk experiment takes `--runs` (default 2) to repeat the scenario set, since there is no automated validator and identical prompts produce meaningfully different responses. `--variant` selects the prompt: `a` is the baseline, `b` is `a` plus a single appended paragraph, so the difference between the two runs is exactly one instruction.

Requires an `ANTHROPIC_API_KEY`. Create a `.env` file in this directory containing:

```
ANTHROPIC_API_KEY=your-key-here
```

## Files

| File | Purpose |
|---|---|
| `config.py` | System prompts, questions, and format experiment definitions |
| `scenarios.json` | The 5 help desk scenarios, kept separate because they are reused in later phases |
| `api.py` | Anthropic client wrapper with token tracking |
| `harness.py` | Runs the selected experiment, validates output, writes results |
| `output/*.md` | The three analysis write-ups (the actual deliverables) |
| `output/*.json` | Raw per-question and per-scenario responses |
