from swinno_bioeconomy_directionality.utils import get_project_root


def test_is_dir():
    assert get_project_root().is_dir()
