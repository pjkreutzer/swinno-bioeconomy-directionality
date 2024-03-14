import pytest
from pathlib import Path
from sqlalchemy import create_engine

from src.swinno_helpers import connect_swinno_db


def test_connect_swinno_db():
    # Mock the get_project_root function
    def mock_get_project_root():
        return Path("/path/to/project/root")

    # Mock the create_engine function
    def mock_create_engine(database_uri):
        return "Mocked engine"

    # Monkey patch the get_project_root and create_engine functions
    connect_swinno_db.get_project_root = mock_get_project_root
    connect_swinno_db.create_engine = mock_create_engine

    # Call the function and assert the result
    engine = connect_swinno_db()
    assert engine == "Mocked engine"

    # Restore the original functions
    connect_swinno_db.get_project_root = Path(get_project_root().parent.absolute())
    connect_swinno_db.create_engine = create_engine

    # Add more test cases if needed
