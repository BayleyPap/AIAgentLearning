# Pydantic Validator

## What It Does
A CLI chatbot that enforces a typed schema on LLM output. The model is instructed
to respond only in JSON. Each response is parsed and validated against a Pydantic
model before being used. Both failure modes — invalid JSON and constraint violations
— are handled explicitly with re-prompting.

## Why I Built It
To practice structured output extraction from LLMs and runtime validation with
Pydantic v2. This pattern appears in every agent project that depends on typed
data from a model.

## How to Run It
```fish
cd phase-1/06-pydantic-validator
python -m venv venv
source venv/bin/activate.fish
pip install anthropic pydantic python-dotenv
cp .env.example .env  # add your ANTHROPIC_API_KEY
python LLMResponse.py
```

## What I Learned
- Pydantic validates types and constraints at runtime, not just statically. A float
  field typed as `float = Field(ge=0.0, le=1.0)` will raise ValidationError if the
  value is 1.8, even though it's a valid float.
- LLMs don't always return clean JSON even when instructed to. A preprocessing step
  to strip markdown code fences before parsing is necessary in practice.
- API errors and validation errors need separate handling — they're different failure
  modes and conflating them produces confusing output.

## What I Would Do Differently
Return a typed result object from `extract_and_validate_json` rather than `None`
on failure, so callers can distinguish between "validation failed" and "API error"
without relying on print side effects.