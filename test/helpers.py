from typing import Any

from hiergen.hiergen import HierGen


def use_HierGen(
    hg: HierGen,
    depth: int = 0,
    output: list[str] | None = None,  # If this is [], then the parallel tests fail
) -> list[str] | None:
    made_output = output is None
    if output is None:
        output = []
    for li in hg:
        content = li.content
        line_no = li.line_no
        start = li.start
        end = li.end
        txt = f"{line_no=}: {content=} {depth=} {start=} {end=}"
        output.append(txt)
        use_HierGen(li.children, depth + 1, output)
    if made_output:
        return output
    return None


def compare_list(actual: list[str], expected: list[str]) -> None:
    for a, e in zip(actual, expected, strict=False):
        assert a == e
    assert len(actual) == len(expected)


def output_actual(actual: list[str]) -> None:
    for _line in actual:
        pass


def deep_compare(actual: Any, expected: Any) -> None:
    assert type(actual) is type(expected)
    if isinstance(actual, list):
        for actual_element, expected_element in zip(actual, expected, strict=False):
            deep_compare(actual_element, expected_element)
    elif isinstance(actual, dict):
        actual_keys = list(actual.keys())
        expected_keys = list(expected.keys())
        deep_compare(actual_keys, expected_keys)
        for key in actual_keys:
            deep_compare(actual[key], expected[key])
    else:
        assert actual == expected
