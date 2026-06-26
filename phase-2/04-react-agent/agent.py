import logging

from api import API
from parser import parse_react_output
from tools import execute_tool

logger = logging.getLogger(__name__)
REMINDER = (
    "Your previous response did not match the required format.\n"
    "Respond in exactly one of these two formats:\n"
    "\n"
    "Thought: <your reasoning>\n"
    'Action: tool_name("input")\n'
    "\n"
    "Or, if you have the final answer:\n"
    "\n"
    "Thought: I now have the answer.\n"
    "Final Answer: <your answer>\n"
    "\n"
    "Arguments must be wrapped in double quotes."
)


def format_observation(text: str) -> str:
    """Format a tool result or system message as an observation."""
    return f"Observation: {text}"


def run_react_loop(question: str, max_iterations: int = 8) -> str:
    """Run the ReAct loop until final answer or a failure condition."""

    if not question.strip():
        return "Input empty, please provide a query"

    api = API()
    messages = []
    messages.append({"role": "user", "content": question})
    consecutive_parse_failures = 0
    for iteration in range(1, max_iterations + 1):
        try:
            response = api.query_anthropic(messages)
        except Exception as e:
            logger.error(f"API error on iteration {iteration}: {e}")
            return f"Loop failed: API error after {iteration - 1} iterations: {e}"

        messages.append({"role": "assistant", "content": response})
        parsed = parse_react_output(response)
        logger.info(
            f"Iteration {iteration}: thought={parsed['thought']!r}, "
            f"action={parsed['action_name']!r}({parsed['action_arg']!r}),"
            f"final={parsed['final_answer']!r}"
        )

        if parsed["final_answer"] is not None:
            return parsed["final_answer"]
        if parsed["action_name"] is None or parsed["action_arg"] is None:
            consecutive_parse_failures += 1
            if consecutive_parse_failures >= 2:
                return "Loop failed: two consecutive parse failures"
            messages.append({"role": "user", "content": format_observation(REMINDER)})
            continue
        consecutive_parse_failures = 0
        tool_result = execute_tool(parsed["action_name"], parsed["action_arg"])
        messages.append({"role": "user", "content": format_observation(tool_result)})
    return (
        f"Loop failed: max iterations ({max_iterations}) reached without final answer"
    )
