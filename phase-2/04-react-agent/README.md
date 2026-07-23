# ReAct Agent

## What It Does

A ReAct agent built from scratch with no frameworks. The model reasons in text (Thought), requests a tool (Action), and the loop executes the tool and feeds the result back (Observation) until the model produces a Final Answer. Two tools: a calculator and a hardcoded fact lookup. Everything between the Anthropic API and the tools is my own code.

## Why I Built It

This pattern sits underneath every agent framework. Building it by hand before touching LangGraph in Phase 4 means I understand what those frameworks abstract away, and it paid off: I found a failure mode (fake tool use, below) that framework users never see because the framework hides it.

## How to Run It

```bash
cd phase-2/04-react-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your ANTHROPIC_API_KEY
python main.py
```

Tests: `pytest -v`. Everything is mocked at module seams, nothing hits the network.

## How the Loop Works

The system prompt forces the model into one of two formats:

```
Thought: <reasoning>
Action: tool_name("input")
```

or, when it is done:

```
Thought: I now have the answer.
Final Answer: <answer>
```

The loop parses each response. An Action gets dispatched to the named tool and the result goes back into the conversation as `Observation: <result>`, then the model is called again. A Final Answer ends the loop. The model never executes anything itself, it only asks.

## Parsing

`parser.py` extracts Thought, Action and Final Answer with `re.search`, not `re.match`. Models add preamble before `Thought:` and an anchored pattern misses it silently. I hit this as a real bug during the build. Only the Final Answer pattern uses `re.DOTALL`, since answers can legitimately span multiple lines.

`parse_action` splits the action line with `(\w+)\("(.+)"\)`, requiring double quotes around the argument, and returns `(None, None)` on anything malformed instead of raising. The parser never touches the API or the tools, so its behaviour is fully verified in isolation by `test_parser.py` before any loop test depends on it.

## Error Handling

Failures the model can cause are fed back to it as Observations, because it can often self-correct:

- Unparseable output gets a reminder restating the exact format. Two consecutive parse failures abort the loop.
- An unknown tool name returns an error string listing the available tools.
- Tool exceptions (like handing the calculator a non-expression) are caught in `execute_tool` and returned as `Tool error:` strings so a bad argument never kills the run.

API errors are the exception: logged, re-raised, and the run ends with a clear message. There is no point continuing a conversation with an API you cannot reach.

The loop caps at 8 iterations so a model that never stops calling tools cannot burn money forever. The calculator uses `simpleeval` rather than `eval` because the input comes from a language model.

## Known Limitation: Fake Tool Use

In roughly 3 of 11 integration test runs, the model emitted both an Action and a Final Answer in a single response:

```
Thought: I can do both.
Action: calculator("2 + 2")
Final Answer: The answer is 4.
```

The loop checks for a Final Answer before an Action, so it returns the answer and never runs the tool. The model did the maths in its head and wrote an Action line it never intended to wait for. In the logs this looks identical to real tool use.

I chose not to patch it. Detecting the both-present case only catches that one shape. It does nothing about the worse version, a fabricated Final Answer with no Action line at all, and a partial fix makes the failure rarer and harder to notice. The problem is structural: any protocol where tool use is plain text the model can imitate is a protocol the model can fake. The fix is native tool calling, where the API itself distinguishes a tool-use block from text. That rebuild is ReAct v3 in Phase 4.

`test_fake_tool_use_known_limitation` pins the current behaviour so any future change is deliberate.

## What I Learned

`re.search` vs `re.match` matters the moment a model adds preamble, which it will. Anchored patterns fail silently, which is the worst way to fail.

`side_effect` lists are how you script a multi-turn conversation against a mocked API, one response per call. `return_value` returns the same thing forever, which is exactly what the max-iterations test wants and what breaks every other test if used by accident.

Feeding tool errors back as Observations lets the model recover on its own far more often than I expected. Crashing on the first bad tool call would have hidden that behaviour entirely.

The fake tool use finding came from testing, not reading. Until I added `final_answer` to the per-iteration log line, there was no visible difference between a real tool run and a faked one.

## What I Would Do Differently

`parse_action` uses a greedy `(.+)` between the quotes, which breaks if an argument ever contains `")`. Fine for two tools with simple inputs, but a lazier match with better anchoring would be more robust.

Tool arguments are a single string, which limits every tool to one parameter. Supporting multiple arguments in a text format means inventing more syntax for the model to get wrong, which is another push towards native tool calling.

The format reminder string lives in `agent.py`. It mirrors the system prompt, so it belongs in `prompts.py` next to the thing it restates.
