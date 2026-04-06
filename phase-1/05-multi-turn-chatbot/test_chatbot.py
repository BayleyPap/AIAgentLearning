import json

import anthropic
import pytest

from chatbot import clear_history, get_input, load_history, save_history, send_message


@pytest.mark.parametrize(
    "invalid_first,valid_second",
    [
        ("x", "valid input"),  # too short
        ("y" * 2001, "valid input"),  # too long
    ],
)
def test_input(mocker, invalid_first, valid_second):
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = [invalid_first, valid_second]

    assert get_input() == valid_second
    assert mock_input.call_count == 2


@pytest.fixture
def mock_client(mocker):
    client = mocker.MagicMock()
    client.messages.create.return_value.content[0].text = "Hello from mock!"
    return client


def test_send_message_returns_text(mock_client):
    result = send_message(mock_client, [{"role": "user", "content": "Hello"}])
    assert result == "Hello from mock!"


def test_send_message_calls_api(mock_client):
    send_message(mock_client, [{"role": "user", "content": "Hello"}])
    mock_client.messages.create.assert_called_once()


def test_api_connection_error(mock_client):
    mock_client.messages.create.side_effect = anthropic.APIConnectionError(request=None)
    result = send_message(mock_client, [{"role": "user", "content": "Hello"}])
    assert result == "Connection failed. Check your network."


def test_rate_limit_error(mocker, mock_client):
    mock_response = mocker.MagicMock()
    mock_client.messages.create.side_effect = anthropic.RateLimitError(
        message=None, body=None, response=mock_response
    )
    result = send_message(mock_client, [{"role": "user", "content": "Hello"}])
    assert result == "Rate limit error please try again later"


def test_api_status_error(mocker, mock_client):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 999
    mock_client.messages.create.side_effect = anthropic.APIStatusError(
        response=mock_response, message="failure 999", body=None
    )
    result = send_message(mock_client, [{"role": "user", "content": "Hello"}])
    assert result == "API error 999: failure 999"


def test_history_length(mock_client):
    history = []
    for x in range(3):
        history.append({"role": "user", "content": "test"})
        assistant_response = send_message(mock_client, history)
        history.append({"role": "assistant", "content": assistant_response})

    assert len(history) == 6


def test_clear_empties_history():
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]
    assert clear_history(history) == 1
    assert history == []


def test_save_history(tmp_path):
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]
    file_path = tmp_path / "test_history"
    save_history(history, str(file_path))
    assert (tmp_path / "test_history.json").exists()
    result = json.loads((tmp_path / "test_history.json").read_text())
    assert result == history


def test_load_history(tmp_path):
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]
    file_path = tmp_path / "test_history"
    (tmp_path / "test_history.json").write_text(json.dumps(history))
    result = load_history(str(file_path))
    assert result == history


def test_load_history_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_history(str(tmp_path / "nonexistent"))


def test_load_history_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not json at all")
    with pytest.raises(ValueError):
        load_history(str(tmp_path / "bad"))
