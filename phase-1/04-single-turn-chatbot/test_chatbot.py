import anthropic
import pytest

from chatbot import get_input, send_message


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
    client.messages.create.return_value.usage.input_tokens = 10
    client.messages.create.return_value.usage.output_tokens = 10
    return client


def test_send_message_returns_text(mock_client):
    result = send_message(mock_client, "Hello")
    assert result == "Hello from mock!"


def test_send_message_calls_api_exactly_once(mock_client):
    send_message(mock_client, "Hello")
    mock_client.messages.create.assert_called_once()


def test_api_connection_error(mock_client):
    mock_client.messages.create.side_effect = anthropic.APIConnectionError(request=None)
    result = send_message(mock_client, "error incoming...")
    assert result == "Connection failed. Check your network."


def test_rate_limit_error(mocker, mock_client):
    mock_response = mocker.MagicMock()
    mock_client.messages.create.side_effect = anthropic.RateLimitError(
        message=None, body=None, response=mock_response
    )
    result = send_message(mock_client, "error incoming...")
    assert result == "Rate limit error please try again later"


def test_api_status_error(mocker, mock_client):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 999
    mock_client.messages.create.side_effect = anthropic.APIStatusError(
        response=mock_response, message="failure 999", body=None
    )
    result = send_message(mock_client, "error incoming...")
    assert result == "API error 999: failure 999"
