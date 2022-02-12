import main
import pytest


@pytest.fixture
def test_get_top_250_data():
    data = main.get_top_250_data()
    assert len(data) == 250


def test_show_dict(results: list[dict], print_file=None):
    for item in results:
        print(item, file=print_file)
