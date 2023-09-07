import shutil
import tempfile
from pathlib import Path
from src.file_utils import create_directory

def test_create_directory():
    # Test that directory is created if it doesn't exist
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir, "test")
        assert not test_dir.exists()
        create_directory(test_dir)
        assert test_dir.exists()

    # Test that directory is not created if it already exists
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir, "test")
        test_dir.mkdir(parents=True)
        assert test_dir.exists()
        create_directory(test_dir)
        assert test_dir.exists()