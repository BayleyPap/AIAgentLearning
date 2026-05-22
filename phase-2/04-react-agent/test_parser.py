from parser import parse_action, parse_react_output
import pytest


@pytest.fixture
def sample_response():
    return {
        "clean_action": 'Thought: I need to calculate this.\nAction: calculator("15 * 7")',
        "clean_final": "Thought: I now have the answer.\nFinal Answer: 105",
        "multiline_final": (
            "Thought: Done.\n"
            "Final Answer: Paris is the capital.\n"
            "Its population is around 2 million."
        ),
        "thought_only": "Thought: I'm just thinking out loud.",
        "both_action_and_final": (
            "Thought: I need to calculate.\n"
            'Action: calculator("5 + 5")\n'
            "Final Answer: 10"
        ),
    }


def test_clean_action_parse(sample_response):
    result = parse_react_output(sample_response["clean_action"])
    assert result["thought"] == "I need to calculate this."
    assert result["action_name"] == "calculator"
    assert result["action_arg"] == "15 * 7"
    assert result["final_answer"] is None


def test_clean_final_answer_parse(sample_response):
    result = parse_react_output(sample_response["clean_final"])
    assert result["thought"] == "I now have the answer."
    assert result["action_name"] is None
    assert result["action_arg"] is None
    assert result["final_answer"] == "105"


def test_multiline_final_parse(sample_response):
    result = parse_react_output(sample_response["multiline_final"])
    assert result["thought"] == "Done."
    assert result["action_name"] is None
    assert result["action_arg"] is None
    assert (
        result["final_answer"]
        == "Paris is the capital.\n" + "Its population is around 2 million."
    )


def test_thought_only_parse(sample_response):
    result = parse_react_output(sample_response["thought_only"])
    assert result["thought"] == "I'm just thinking out loud."
    assert result["action_name"] is None
    assert result["action_arg"] is None
    assert result["final_answer"] is None


def test_both_action_and_final_parse(sample_response):
    result = parse_react_output(sample_response["both_action_and_final"])
    assert result["thought"] == "I need to calculate."
    assert result["action_name"] == "calculator"
    assert result["action_arg"] == "5 + 5"
    assert result["final_answer"] == "10"


def test_valid_inputs_parse_action():
    tool, args = parse_action('calculator("15 * 7")')
    assert tool == "calculator"
    assert args == "15 * 7"


@pytest.mark.parametrize(
    "malformed_input",
    [
        "calculator 15 * 7",  # no parens
        "calculator(15 * 7)",  # no quotes
        "not a tool call at all",  # no structure
        "",  # empty
    ],
)
def test_malformed_input_parse_action(malformed_input):
    tool, arg = parse_action(malformed_input)
    assert tool is None
    assert arg is None


def test_strip_whitespace_parse_action():
    tool, args = parse_action('calculator(" 15 * 7   ")')
    assert tool == "calculator"
    assert args == "15 * 7"
