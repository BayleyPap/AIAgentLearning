import pytest

from transformer import add_timestamp, filter_by_records, read, summary, write


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "name": "Alice", "category": "A", "value": 15},
        {"id": 2, "name": "Bob", "category": "B", "value": 5},
        {"id": 3, "name": "Carol", "category": "A", "value": 20},
        {"id": 4, "name": "Dave", "category": "B", "value": 3},
        {"id": 5, "name": "Eve", "category": "A", "value": 12},
    ]


def test_output_only_contains_high_values(sample_data):
    result = filter_by_records(sample_data, 10)
    assert all(item["value"] >= 10 for item in result)


def test_summary():
    before = [1, 2, 3, 4, 5]
    after = [1, 2, 3]
    result = summary(before, after)
    assert result["total_input"] == 5
    assert result["total_output"] == 3
    assert result["filtered_out"] == 2


def test_output_file_is_created(sample_data, tmp_path):
    output_file = tmp_path / "output.json"
    write(sample_data, output_file)

    assert output_file.exists()


def test_timestamps_added(sample_data):
    sample_data = add_timestamp(sample_data)
    assert all("timestamp" in item for item in sample_data)


def test_read_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        read(tmp_path / "nonexistent.json")


def test_read_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("this is not json")
    with pytest.raises(ValueError):
        read(bad_file)


def test_write_missing_parent(tmp_path):
    with pytest.raises(FileNotFoundError):
        write([], tmp_path / "nonexistent_dir" / "output.json")
