import pytest

from agent import run_react_loop


@pytest.fixture
def mock_api(mocker):
    return mocker.patch("api.API.query_anthropic")


def test_single_tool_completion(mock_api):
    mock_api.side_effect = [
        'Thought: I need to calculate this.\nAction: calculator("15 * 7")',
        "Thought: I now have the answer.\nFinal Answer: 105",
    ]
    result = run_react_loop("What is 15 times 7?")
    assert "105" in result
    assert mock_api.call_count == 2


def test_multi_step_completion(mock_api):
    mock_api.side_effect = [
        'Thought: I need to look up melbourne population.\nAction: lookup("population of melbourne")',
        'Thought: I now need to multiply it by 3.\nAction: calculator("5200000 * 3")',
        "Thought: I now have the answer.\nFinal Answer: 15600000",
    ]
    result = run_react_loop("What is the population of melbourne multiplied by 3?")
    assert "15600000" in result
    assert mock_api.call_count == 3


def test_max_iterations_reached(mock_api):
    mock_api.return_value = 'Thought: Looping.\nAction: calculator("1+1")'
    result = run_react_loop("What is 1+1?")
    assert "max iterations (8) reached" in result
    assert mock_api.call_count == 8


def test_unparsable_output_recovery(mock_api):
    mock_api.side_effect = [
        "this is not parsable",
        "Thought: Recovered.\nFinal Answer: 2",
    ]
    result = run_react_loop("What is 1+1?")
    assert mock_api.call_count == 2
    conversation = " ".join(
        msg["content"] for msg in mock_api.call_args_list[-1].args[0]
    )
    assert "did not match the required format" in conversation
    assert "2" in result


def test_unknown_tool_handled(mock_api):
    mock_api.return_value = (
        'Thought: lets do a bad tool call.\nAction: converse("test")'
    )
    result = run_react_loop("Conduct a bad tool call")
    conversation = " ".join(
        msg["content"] for msg in mock_api.call_args_list[-1].args[0]
    )
    assert "Unknown tool 'converse'" in conversation
    assert mock_api.call_count == 8


def test_tool_execution_error(mock_api):
    mock_api.return_value = (
        'Thought: lets do a bad calculator call.\nAction: calculator("test")'
    )
    result = run_react_loop("Conduct a bad calculator call")
    conversation = " ".join(
        msg["content"] for msg in mock_api.call_args_list[-1].args[0]
    )
    assert "Tool error:" in conversation
    assert mock_api.call_count == 8


def test_fake_tool_use_known_limitation(mocker, mock_api):
    """KNOWN LIMITATION of text-parsed ReAct, documented in the README.

    When the model emits both an Action and a Final Answer in one response,
    the loop's precedence (final_answer checked first) returns the Final
    Answer and never dispatches the tool. This test pins the current
    behavior so any future change is deliberate. Observed in ~3 of 11
    integration tests. Structural fix: native tool calling (ReAct v3,
    Phase 4).
    """
    mock_execute = mocker.patch("agent.execute_tool")
    mock_api.return_value = (
        'Thought: I can do both.\nAction: calculator("2 + 2")\nFinal Answer: 4'
    )
    result = run_react_loop("What is two plus two?")
    assert "4" in result
    mock_execute.assert_not_called()


def test_empty_question_guard(mock_api):
    result = run_react_loop("")
    mock_api.assert_not_called()
    assert "empty" in result.lower()
