from .helpers import deep_compare


def test_deep_compare() -> None:
    expected = {
        "asdf": [1, 2, 3],
        "zxcv": {
            "qwer": 4,
        },
    }
    actual = {
        "asdf": [1, 2],
        "zxcv": {
            "qwer": 4,
        },
    }

    deep_compare(actual, actual)
    deep_compare(expected, expected)
