from llm_response import extract_and_validate_json, llm_response, send_message


def test_valid_response(mocker):
    client = mocker.MagicMock()
    client.messages.create.return_value.content[
        0
    ].text = '{"answer": "Paris", "confidence": 0.9, "sources_needed": false}'
    result = extract_and_validate_json(send_message(client, "prompt"))
    assert isinstance(result, llm_response)


def test_invalid_json(mocker):
    client = mocker.MagicMock()
    client.messages.create.return_value.content[0].text = "not valid json"
    result = extract_and_validate_json(send_message(client, "prompt"))
    assert result is None


def test_validation_error(mocker):
    client = mocker.MagicMock()
    client.messages.create.return_value.content[
        0
    ].text = '{"answer": "Paris", "confidence": 17.2, "sources_needed": false}'
    result = extract_and_validate_json(send_message(client, "prompt"))
    assert result is None
