import re


def parse_react_output(text: str) -> dict:
    """Pulls structured data from LLM output"""
    thought_match = re.search(r"Thought:\s*(.+)", text)
    action_match = re.search(r"Action:\s*(.+)", text)
    final_match = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL)

    thought = thought_match.group(1).strip() if thought_match else None
    action_line = action_match.group(1).strip() if action_match else None
    final_answer = final_match.group(1).strip() if final_match else None

    action_name, action_arg = parse_action(action_line) if action_line else (None, None)

    return {
        "thought": thought,
        "action_name": action_name,
        "action_arg": action_arg,
        "final_answer": final_answer,
    }


def parse_action(action_line: str) -> tuple[str | None, str | None]:
    """Splits the action string into tool name and arguments for the tool"""
    match = re.search(r'(\w+)\("(.+)"\)', action_line)
    if match is None:
        return None, None
    return match.group(1), match.group(2).strip()
