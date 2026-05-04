# Experiment 1: Persona and Tone Control

Tested whether system prompts can reliably control persona, tone, and behavioural constraints across 3 personas and 5 questions (15 total responses) using claude-haiku-4-5.

## System Prompts

**Terse expert:**
> You are a senior Linux engineer. Answer only with commands and one-sentence explanations. Never use bullet points or numbered lists. Never say "certainly", "of course", "great question", or any acknowledgement of the question. Get straight to the answer.

**Patient teacher:**
> You are a patient teacher explaining concepts to a complete beginner. Use at least one analogy in every response. End every response with one follow-up question that checks understanding. Never use technical jargon without defining it the first time it appears.

**Devil's advocate:**
> You always argue against whatever position the user states or implies. Be intellectually honest and cite specific reasons, but always take the opposing view. If the user is neutral, argue against the most common default position on the topic.

## Results

### Terse expert

| Q | In character | Violations |
|---|---|---|
| Q1 port 8080 | Partial | used markdown headers/code fences as visual structure but no bullets, fine |
| Q2 grep python | Yes | clean |
| Q3 SQLite vs PG | Partial | one massive run-on sentence, technically followed "one-sentence" rule but unreadable |
| Q4 code review | No | used bullet points (the entire response is bulleted via paragraph breaks acting as items) |
| Q5 Rust 2026 | Partial | bizarre fake bash command at top, but the actual answer is one sentence |

### Patient teacher

| Q | In character | Violations |
|---|---|---|
| Q1 port 8080 | Yes | analogy (apartment mailboxes), follow-up question, defines terms |
| Q2 grep python | Partial | said "Great question" which isn't forbidden here but worth noting, otherwise compliant |
| Q3 SQLite vs PG | Partial | "Great question" again, otherwise good (bicycle/car analogy, follow-up question) |
| Q4 code review | Yes | proofreading analogy, follow-up question, used numbered list which wasn't forbidden |
| Q5 Rust 2026 | Partial | "Great question" again, cast iron analogy, follow-up question |

### Devil's advocate

| Q | In character | Violations |
|---|---|---|
| Q1 port 8080 | Yes | argues against finding the process at all, gives the answer reluctantly |
| Q2 grep python | Yes | argues grep is wrong tool, recommends find/fd |
| Q3 SQLite vs PG | Yes | argues against SQLite (the conventional small-project answer) |
| Q4 code review | Yes | argues against the premise that code review skill matters |
| Q5 Rust 2026 | Yes | argues against learning Rust, recommends Go instead |

## Analysis

The Devil's Advocate persona was the most reliable, holding character on all 5 responses without exception. The constraint was simple, behavioural, and didn't fight against the model's natural verbosity. It also benefits from being framed positively ("always argue against") rather than as a list of prohibitions.

The Patient Teacher held character on the substantive constraints (analogies, follow-up questions, defined jargon) but repeatedly violated the "no acknowledgements" pattern by opening with "Great question" 3 times out of 5. Notably, this isn't actually in its system prompt, only the Terse Expert prompt forbids that. So technically zero violations, but it shows the model defaults to that opener unless explicitly told not to.

The Terse Expert was the least reliable. The "never use bullet points or numbered lists" constraint broke on Q4, where the model produced what is functionally a bulleted list using paragraph breaks. The "one-sentence explanations" rule was technically followed on Q3 by producing a single grammatically valid run-on sentence, which defeats the spirit of the constraint. Q5 produced an inexplicable hallucinated bash command before the actual answer, suggesting the model was reaching for "be a Linux engineer" so hard it invented commands that don't make sense.

Three takeaways for Phase 4 agent prompts:

1. **Negative constraints (never do X) are weaker than positive constraints (always do Y).** The Terse Expert's prohibitions broke more often than the Devil's Advocate's positive framing.

2. **The model interprets constraints semantically, not literally.** "One sentence" became "one grammatically valid sentence with five clauses," which technically satisfies the rule. Specifying constraints needs to anticipate this loophole-finding behaviour.

3. **Default behaviours leak through.** The "Great question" opener appeared in the persona that didn't forbid it but never appeared in the one that did. When designing agents, assume the model will fall back to defaults unless explicitly redirected.
