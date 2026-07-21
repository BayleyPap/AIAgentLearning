# Experiment 3: Help Desk Persona and Escalation Behaviour

Tested whether a system prompt can control escalation behaviour in a support agent: whether the model commits to an action, hands the ticket off, or stalls. Two prompt variants across 5 scenarios, 2 runs each (20 total responses) using claude-haiku-4-5.

Unlike Experiments 1 and 2 there is no automated validator. Scoring is manual and author-scored, which is a real limitation given the sample size. Variance is addressed by running every scenario twice rather than by a larger n.

## The Scenarios

Five help desk tickets written in user voice, held in `scenarios.json` at the project root. They are deliberately vague and incomplete, the way tickets actually arrive. The set is reused: it seeds the 30-scenario evaluation set in Phase 3 and the fine-tuning evaluation set in Phase 5, so it lives in JSON rather than in `config.py`.

| ID | Scenario | Expected type |
|---|---|---|
| 1 | Opaque vendor error code on a card payment terminal | escalate |
| 2 | Receipt printer not detected on one register | answerable |
| 3 | Register frozen, no keyboard input, after a power flicker | answerable |
| 4 | New starter, Outlook fails, other Citrix apps fine | escalate |
| 5 | Scanner not scanning, no other detail | ambiguous |

Scenario 1 is the fabrication test. There is no corpus in this experiment, so the model has no way to know what the code means. Scenario 4 is the hardest pass: correct behaviour is partial diagnosis followed by a handoff, not a flat refusal. Scenario 5 has no single right answer and the correct first move is a clarifying question.

## System Prompts

**Variant A (baseline):**
> You are a senior help desk technician supporting store staff at a large retail company. Before suggesting any action, state what you are checking and why. Establish the scope of a problem before proposing a fix: whether it affects one device or several, and what changed.
>
> Your only capabilities are advising staff over the phone and rebooting a POS terminal remotely. Escalate, rather than advise, when a fix would require administrator rights, a change to an account or mailbox, a server-side change, physical access to hardware, or interpretation of a vendor-specific error code you do not have documentation for.
>
> When you escalate, say what you have established so far, what you need from the user, and which team the ticket goes to.

**Variant B (single-turn bound):** variant A plus one appended paragraph, so the diff between the two is exactly one instruction.
> You get one response. The user is not able to answer questions before you act. Every response ends with a decision: either the specific action you are advising the user to take now, or an escalation with the team it goes to. Where you need information you do not have, state your best assessment on the information given, name what would change it, and include the questions alongside the decision rather than in place of it.

## Results

Scored on three axes. **Committed** means the response ends in an action or an escalation rather than a conditional promise. **Fabricated** means the response asserted something it had no basis for. **Correct** applies only where a decision was made.

### Variant A

| Scenario | Run | Committed | Fabricated | Notes |
|---|---|---|---|---|
| 1 vendor code | 1 | No | No | Asks whether "Terminal Error 1" is the complete message, which is the right instinct |
| 1 vendor code | 2 | No | No | Names the code as processor-specific, gates everything on scope |
| 2 printer | 1 | No | No | Good checks listed, none advised as an action |
| 2 printer | 2 | No | No | Same |
| 3 frozen register | 1 | No | No | Correctly escalates to a known-good keyboard swap as a next step |
| 3 frozen register | 2 | No | No | Acknowledges the reseat already done, then asks the user to check the cable is seated |
| 4 new starter | 1 | No | No | Reaches "account or mailbox" as a possibility, does not escalate |
| 4 new starter | 2 | No | No | Same |
| 5 scanner | 1 | No | No | Six clarifying questions |
| 5 scanner | 2 | No | No | Five clarifying questions |

Commitment: 0 of 10. Every response is a numbered list of scope questions closing with a conditional promise to either advise or escalate once the user answers.

### Variant B

| Scenario | Run | Committed | Fabricated | Correct |
|---|---|---|---|---|
| 1 vendor code | 1 | No | **Yes** | n/a |
| 1 vendor code | 2 | No | **Yes** | n/a |
| 2 printer | 1 | Yes | No | Yes |
| 2 printer | 2 | Yes | No | Yes |
| 3 frozen register | 1 | No | No | n/a |
| 3 frozen register | 2 | Yes | No | Yes |
| 4 new starter | 1 | Yes | No | Yes |
| 4 new starter | 2 | Yes | No | Yes |
| 5 scanner | 1 | No | No | n/a |
| 5 scanner | 2 | No | No | n/a |

Commitment: 5 of 10. Fabrication: 2 of 10, both on scenario 1.

### Scenario 5 and the instruction conflict

Both B runs of scenario 5 refused to commit and asked clarifying questions instead. That violates the turn bound and is also the correct help desk behaviour on a genuinely ambiguous ticket. Scored as instruction violation, correct behaviour. It is evidence that a hard turn bound is the wrong constraint for this scenario class rather than evidence of a model defect.

### Default leakage

Markdown headers, bold, and numbered lists appear in all 20 responses despite neither prompt requesting them. "Welcome to the team!" opens both A runs of scenario 4 and neither B run, so a competing structural instruction displaces the default rather than the default being absent.

## Analysis

Experiment 3 tested whether a system prompt can control escalation behaviour: whether the model decides, defers, or invents. Two variants, five scenarios, two runs each.

Variant A never reached a decision. All ten responses asked scope questions and closed with a conditional promise to advise or escalate once the user answered. The escalation criteria written into the prompt were never exercised, because nothing got far enough to trigger them. That is a design error in the prompt rather than a model failure: "establish the scope of a problem before proposing a fix" is unbounded in a single turn, so scope-gathering consumed every response.

Variant B added one paragraph binding the model to a single turn and requiring every response to end in an action or an escalation. Commitment went from zero to five of ten, and it tracked the scenario rather than the instruction. The model committed where a safe generic action existed (power cycle the printer) or where the escalation trigger was unambiguous (new starter, Outlook only, mailbox provisioning). It stalled where the diagnosis was genuinely underdetermined.

Two failures matter more than the commit rate.

The first is the decision-shaped deferral. Several B responses print a Decision heading and then defer underneath it, promising to reboot or escalate once the user answers two more questions. That is the Experiment 1 finding in a third domain: the model satisfies the visible shape of a constraint while defeating its intent.

The second is fabrication under pressure. Asked about an opaque vendor error code, variant A correctly probed whether the displayed message was complete. Variant B produced a confident list of likely causes for a code it has no way to know, and still did not commit to a decision. The prompt named that exact escalation trigger and the model walked past it.

Structural compliance held at ten out of ten across both variants, consistent with Experiments 1 and 2.

## Known Limitations of This Experiment

**Single turn.** An escalation decision is naturally a second-turn behaviour, and testing it in one turn was a design error. Variant B works around it with an instruction rather than fixing it with a conversation. A multi-turn version where a scripted user answers the first round of questions would measure the real behaviour.

**Author-scored, small n.** Five scenarios, two runs, one scorer who also wrote the prompt and the scenarios. The commit and fabrication axes are close to objective. The correctness axis is not.

**No corpus.** The model answers from parametric knowledge only, so "answerable" here means answerable from general troubleshooting knowledge. Phase 3 adds a document corpus and a `gold_source` field per scenario, at which point retrieval hit rate becomes measurable and these results become the pre-RAG baseline.

## What This Feeds

The fabrication result is the reason the Phase 3 evaluation set carries escalate scenarios and a decline rate metric. A support bot under pressure to produce an answer will invent one, and it will do so most readily on exactly the inputs where it has least basis. Measuring pass rate alone would not have caught it.
