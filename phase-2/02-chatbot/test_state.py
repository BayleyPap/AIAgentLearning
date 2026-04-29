import json

import pytest

from state import State


# Happy path tests
def test_get_history_returns_copy():
    my_state = State()
    my_state.add_turn(
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    )
    new_list = my_state.get_history()
    new_list.append({"role": "user", "content": "Hello"})
    assert len(my_state) == 1
    assert len(new_list) == 3


def test_add_turn():
    my_state = State()
    my_state.add_turn(
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    )
    my_state.add_turn(
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    )
    assert len(my_state) == 2


def test_state_clear():
    my_state = State()
    my_state.add_turn(
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    )
    assert my_state.clear_history() == 1
    assert my_state.get_history() == []


def test_state_import(tmp_path):
    my_state = State()
    my_state.add_turn(
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    )
    file_path = tmp_path / "test_history.json"
    (tmp_path / "test_history.json").write_text(json.dumps(my_state.get_history()))
    new_state = State()
    new_state.import_history(file_path)
    assert new_state.get_history() == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]


def test_state_export(tmp_path):
    my_state = State()
    my_state.add_turn(
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    )
    file_path = tmp_path / "test_history.json"
    my_state.export_history(file_path)
    assert (tmp_path / "test_history.json").exists()
    result = json.loads((tmp_path / "test_history.json").read_text())
    assert result == [
        {"role": "user", "content": "Hello"},
        {
            "role": "assistant",
            "content": "Hi there",
        },
    ]


def test_state_summary():
    my_state = State()
    my_state.add_turn(
        {"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi"}
    )
    assert (
        my_state.get_summary() == "Conversation ended. 1 turns, 7 characters exchanged."
    )


# Failure path tests


def test_missing_import_file(tmp_path):
    my_state = State()
    with pytest.raises(FileNotFoundError):
        my_state.import_history(tmp_path / "nonexistent")


def test_invalid_import_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not json at all")
    my_state = State()
    with pytest.raises(ValueError):
        my_state.import_history(tmp_path / "bad.json")


def test_invalid_export_path(tmp_path):
    my_state = State()
    with pytest.raises(FileNotFoundError):
        my_state.export_history(tmp_path / "nonexistent_dir" / "nonexistent")


def test_invalid_import_datatype(tmp_path):
    file_path = tmp_path / "test_history.json"
    (tmp_path / "test_history.json").write_text(
        json.dumps({"role": "user", "content": "hello"})
    )
    new_state = State()
    with pytest.raises(TypeError):
        new_state.import_history(file_path)


def test_get_formatted_history():
    my_state = State()
    my_state.add_turn(
        {"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi"}
    )
    assert (
        my_state.get_history_formatted()
        == "Chat history:\nuser: hello\nassistant: hi\n"
    )
