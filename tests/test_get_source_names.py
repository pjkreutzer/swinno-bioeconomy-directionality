import os
import tempfile
from collections import defaultdict
import pytest
from src.file_utils import get_source_names

def test_get_source_names():
    with tempfile.TemporaryDirectory() as temp_dir:
        lookup_path = os.path.join(temp_dir, "lookup.txt")
        with open(lookup_path, "w") as f:
            f.write("1|source1\n")
            f.write("2|source2\n")
            f.write("3|source3\n")

        input_ids = ["1", "3", "4"]
        expected_output = {"1": ["source1"], "3": ["source3"]}
        output = get_source_names(lookup_path, input_ids)
        assert output == expected_output

def test_get_source_names_empty_input():
    with tempfile.TemporaryDirectory() as temp_dir:
        lookup_path = os.path.join(temp_dir, "lookup.txt")
        with open(lookup_path, "w") as f:
            f.write("1|source1\n")
            f.write("2|source2\n")
            f.write("3|source3\n")

        input_ids = []
        expected_output = {}
        output = get_source_names(lookup_path, input_ids)
        assert output == expected_output

def test_get_source_names_invalid_file():
    input_ids = ["1", "2", "3"]
    with tempfile.TemporaryDirectory() as temp_dir:
        lookup_path = os.path.join(temp_dir, "lookup.txt")
        with open(lookup_path, "w") as f:
            f.write("1|source1\n")
            f.write("2|source2\n")
            f.write("3|source3\n")

        os.remove(lookup_path)
        with pytest.raises(Exception):
            get_source_names(lookup_path, input_ids)