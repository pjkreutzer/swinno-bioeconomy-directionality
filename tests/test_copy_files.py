import os
import tempfile
from pathlib import Path
from shutil import copy
from unittest.mock import patch, MagicMock
from src.file_utils import copy_files

def test_copy_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir, "source")
        destination_dir = Path(temp_dir, "destination")
        os.makedirs(source_dir, exist_ok=True)
        os.makedirs(destination_dir, exist_ok=True)

        source_file1 = Path(source_dir, "file1.jpg")
        source_file2 = Path(source_dir, "file2.jpg")
        destination_file1 = Path(destination_dir, "images", "id1", "file1.jpg")
        destination_file2 = Path(destination_dir, "images", "id1", "file2.jpg")

        source_file1.touch()
        source_file2.touch()

        copy_files("id1", ["file1", "file2"], source_dir, destination_dir)

        assert destination_file1.exists()
        assert destination_file2.exists()

def test_copy_files_permission_error():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir, "source")
        destination_dir = Path(temp_dir, "destination")
        os.makedirs(source_dir, exist_ok=True)
        os.makedirs(destination_dir, exist_ok=True)

        source_file1 = Path(source_dir, "file1.jpg")
        destination_file1 = Path(destination_dir, "images", "id1", "file1.jpg")

        source_file1.touch()
        destination_file1.touch()

        with patch("shutil.copy", MagicMock(side_effect=PermissionError)):
            with patch("builtins.print") as mock_print:
                copy_files("id1", ["file1"], source_dir, destination_dir)
                mock_print.assert_called_with(f"Error: Permission denied when copying {source_file1} to {destination_file1}")

def test_copy_files_no_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir, "source")
        destination_dir = Path(temp_dir, "destination")
        os.makedirs(source_dir, exist_ok=True)
        os.makedirs(destination_dir, exist_ok=True)

        copy_files("id1", ["file1"], source_dir, destination_dir)

        assert not Path(destination_dir, "images", "id1").exists()