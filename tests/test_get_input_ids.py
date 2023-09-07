import pytest
from pathlib import Path
from src.file_utils import get_input_ids

@pytest.fixture
def input_file(tmp_path):
    input_data = [
        5874001,
        5880001,
        5881001,
        5883001,
        5886001,
        5894001,
        5897001,
        5910001,
        5920001,
        5928001,
    ]
    input_file = tmp_path / "input.txt"
    with open(input_file, "w") as f:
        f.write("\n".join(str(id) for id in input_data))
    return input_file

def test_get_input_ids(input_file):
    # Test that function returns expected IDs
    expected_ids = [
        "5874",
        "5880",
        "5881",
        "5883",
        "5886",
        "5894",
        "5897",
        "5910",
        "5920",
        "5928",
    ]
    assert get_input_ids(input_file) == expected_ids