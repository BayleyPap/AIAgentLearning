import anthropic
import pytest

from api import API


@pytest.fixture
def mock_client(mocker):
    client = mocker.MagicMock()
    client.messages.create.return_value.content[0].text = "Hello from mock!"
    client.messages.create.return_value.usage.input_tokens = 10
    client.messages.create.return_value.usage.output_tokens = 10
    return client


@pytest.fixture
def api(mock_client):
    instance = API()
    instance.client = mock_client
    return instance


def test_send_message_returns_text(api):
    result = api.query_anthropic([{"role": "user", "content": "Hello"}])
    assert result == "Hello from mock!"


def test_send_message_calls_api_exactly_once(api):
    api.query_anthropic([{"role": "user", "content": "Hello"}])
    api.client.messages.create.assert_called_once()


def test_api_connection_error(api):
    api.client.messages.create.side_effect = anthropic.APIConnectionError(request=None)
    with pytest.raises(anthropic.APIConnectionError):
        api.query_anthropic([{"role": "user", "content": "Hello"}])


def test_rate_limit_error(mocker, api):
    mock_response = mocker.MagicMock()
    api.client.messages.create.side_effect = anthropic.RateLimitError(
        message=None, body=None, response=mock_response
    )
    with pytest.raises(anthropic.RateLimitError):
        api.query_anthropic([{"role": "user", "content": "Hello"}])


def test_api_status_error(mocker, api):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 999
    api.client.messages.create.side_effect = anthropic.APIStatusError(
        response=mock_response, message="failure 999", body=None
    )
    with pytest.raises(anthropic.APIStatusError):
        api.query_anthropic([{"role": "user", "content": "Hello"}])
