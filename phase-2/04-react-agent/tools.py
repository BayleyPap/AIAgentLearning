from typing import Callable

from simpleeval import simple_eval


def calculator(arg: str) -> str:
    """Evaluate a math expression and return the result as a string."""
    result = simple_eval(arg)
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)


FACTS = {
    "capital of france": "Paris",
    "capital of japan": "Tokyo",
    "capital of australia": "Canberra",
    "capital of uk": "London",
    "population of france": "68000000",
    "population of australia": "26000000",
    "population of melbourne": "5200000",
    "population of tokyo": "14000000",
    "population of usa": "333000000",
    "distance earth to moon": "384400 km",
    "distance sydney to melbourne": "878 km",
    "speed of light": "299792458 m/s",
}


def lookup(arg: str) -> str:
    """Look up a fact from the hardcoded knowledge base."""
    key = arg.strip().lower()
    return FACTS.get(key, f"No information found for: {arg}")


TOOLS: dict[str, Callable[[str], str]] = {"calculator": calculator, "lookup": lookup}


def execute_tool(tool_name: str, arg: str) -> str:
    """Dispatch to the named tool and return its result, or a clean error string."""
    if tool_name not in TOOLS:
        return f"Unknown tool '{tool_name}'. Available: {', '.join(TOOLS)}"

    try:
        return TOOLS[tool_name](arg)
    except Exception as e:
        return f"Tool error: {e}"
