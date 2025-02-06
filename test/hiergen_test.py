from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from hiergen.comments import HashtagCommentFinder, _CommentFinder
from hiergen.exceptions import (
    HierGenInvalidCommentFinderError,
    HiergenInvalidLineSourceError,
)
from hiergen.hiergen import HierGen

from .helpers import compare_list, output_actual, use_HierGen


def _test(lines: str, expected: str, comment_finder: _CommentFinder | None = None) -> None:
    hg = HierGen.from_line_with_newlines(lines, comment_finder=comment_finder)
    actual = use_HierGen(hg)
    output_actual(actual)
    compare_list(actual, expected.splitlines()[1:])


def test_empty() -> None:
    lines = """
"""
    expected = """
"""
    _test(lines, expected)


def test_one_layer() -> None:
    lines = """
A
B
C"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=3: content='B' depth=0 start=0 end=1
line_no=4: content='C' depth=0 start=0 end=1
"""
    _test(lines, expected)


def test_two_layer() -> None:
    lines = """
A
    B
C
    D
E
    F"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=3: content='B' depth=1 start=4 end=5
line_no=4: content='C' depth=0 start=0 end=1
line_no=5: content='D' depth=1 start=4 end=5
line_no=6: content='E' depth=0 start=0 end=1
line_no=7: content='F' depth=1 start=4 end=5
"""
    _test(lines, expected)


def test_three_layer() -> None:
    lines = """
A
    B
C
    D
        E
F
    G
        H"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=3: content='B' depth=1 start=4 end=5
line_no=4: content='C' depth=0 start=0 end=1
line_no=5: content='D' depth=1 start=4 end=5
line_no=6: content='E' depth=2 start=8 end=9
line_no=7: content='F' depth=0 start=0 end=1
line_no=8: content='G' depth=1 start=4 end=5
line_no=9: content='H' depth=2 start=8 end=9
"""
    _test(lines, expected)


def test_sudden_layer_drop() -> None:
    lines = """
A
    B
        C
            D
E
"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=3: content='B' depth=1 start=4 end=5
line_no=4: content='C' depth=2 start=8 end=9
line_no=5: content='D' depth=3 start=12 end=13
line_no=6: content='E' depth=0 start=0 end=1
"""
    _test(lines, expected)


def test_end_on_child_layer() -> None:
    lines = """
A
    B
        C
            D
"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=3: content='B' depth=1 start=4 end=5
line_no=4: content='C' depth=2 start=8 end=9
line_no=5: content='D' depth=3 start=12 end=13
"""
    _test(lines, expected)


def test_end_on_root_layer() -> None:
    lines = """
A
    B
        C
            D
E
"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=3: content='B' depth=1 start=4 end=5
line_no=4: content='C' depth=2 start=8 end=9
line_no=5: content='D' depth=3 start=12 end=13
line_no=6: content='E' depth=0 start=0 end=1
"""
    _test(lines, expected)


def test_blank_lines() -> None:
    lines = """
A

    B
        C

            D

    E

        F
"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=4: content='B' depth=1 start=4 end=5
line_no=5: content='C' depth=2 start=8 end=9
line_no=7: content='D' depth=3 start=12 end=13
line_no=9: content='E' depth=1 start=4 end=5
line_no=11: content='F' depth=2 start=8 end=9
"""
    _test(lines, expected)


def test_commments() -> None:
    lines = """
A
# asdf
    B  # zxcv
        C

            D
# asdf
    E

        F # asdf
    # asdfgas
# asf
"""
    expected = """
line_no=2: content='A' depth=0 start=0 end=1
line_no=4: content='B  ' depth=1 start=4 end=7
line_no=5: content='C' depth=2 start=8 end=9
line_no=7: content='D' depth=3 start=12 end=13
line_no=9: content='E' depth=1 start=4 end=5
line_no=11: content='F ' depth=2 start=8 end=10
"""
    _test(lines, expected, HashtagCommentFinder())


# Factories section

LINES = """A
B
    C
D
E
    F
        G
H
    """

EXPECTED = [
    "line_no=1: content='A' depth=0 start=0 end=1",
    "line_no=2: content='B' depth=0 start=0 end=1",
    "line_no=3: content='C' depth=1 start=4 end=5",
    "line_no=4: content='D' depth=0 start=0 end=1",
    "line_no=5: content='E' depth=0 start=0 end=1",
    "line_no=6: content='F' depth=1 start=4 end=5",
    "line_no=7: content='G' depth=2 start=8 end=9",
    "line_no=8: content='H' depth=0 start=0 end=1",
]


def test_from_line_generator() -> None:
    def line_gen(lines: list[str]) -> Generator[tuple[str, int]]:
        for line_no, line in enumerate(lines, start=1):
            yield line, line_no

    lines = LINES.splitlines()
    lg = line_gen(lines)
    hg = HierGen.from_line_generator(lg)
    actual = use_HierGen(hg)
    compare_list(actual, EXPECTED)


def test_from_list_of_str() -> None:
    lines = LINES.splitlines()
    hg = HierGen.from_line_list(lines)
    actual = use_HierGen(hg)
    compare_list(actual, EXPECTED)


def test_from_str_with_newlines() -> None:
    hg = HierGen.from_line_with_newlines(LINES)
    actual = use_HierGen(hg)
    compare_list(actual, EXPECTED)


def test_from_text_file() -> None:
    with NamedTemporaryFile(mode="w", delete=True, delete_on_close=False) as f:
        f.write(LINES)
        f.close()
        fp = Path(f.name)
        hg = HierGen.from_text_file(fp)
        actual = use_HierGen(hg)
        compare_list(actual, EXPECTED)


def test_from_line_generator_via_any() -> None:
    def line_gen(lines: list[str]) -> Generator[tuple[str, int]]:
        for line_no, line in enumerate(lines, start=1):
            yield line, line_no

    lines = LINES.splitlines()
    lg = line_gen(lines)
    hg = HierGen.from_any(lg)
    actual = use_HierGen(hg)
    compare_list(actual, EXPECTED)


def test_from_list_of_str_via_any() -> None:
    lines = LINES.splitlines()
    hg = HierGen.from_any(lines)
    actual = use_HierGen(hg)
    compare_list(actual, EXPECTED)


def test_from_str_with_newlines_via_any() -> None:
    hg = HierGen.from_any(LINES)
    actual = use_HierGen(hg)
    compare_list(actual, EXPECTED)


def test_from_text_file_via_any() -> None:
    with NamedTemporaryFile(mode="w", delete=True, delete_on_close=False) as f:
        f.write(LINES)
        f.close()
        fp = Path(f.name)
        hg = HierGen.from_any(fp)
        actual = use_HierGen(hg)
        compare_list(actual, EXPECTED)


def test_from_int_via_any() -> None:
    with pytest.raises(
        HiergenInvalidLineSourceError,
        match="Cannot use line source of type .*",
    ):
        HierGen.from_any(1)  # type: ignore[arg-type]


def test_skips_unconsumed_children() -> None:
    lines = """
A
    aa
B
    bb
        cc
    dd
C
    ee"""
    expected = [
        "A",
        "B",
        "C",
    ]
    hg = HierGen.from_any(lines)
    actual = [li.line for li in hg]
    compare_list(actual, expected)


def test_is_empty_on_no_children() -> None:
    lines = """
A
    B
C
"""
    hg = HierGen.from_line_with_newlines(lines)
    li = hg.next()
    assert not li.children.is_empty
    li = hg.next()
    assert li.children.is_empty


def test_create_tokenizer() -> None:
    lines = """
asdf ghjk # QWER
"""
    source = "test_create_tokenizer"
    hg = HierGen.from_line_with_newlines(
        lines,
        source_name=source,
        comment_finder=HashtagCommentFinder(),
    )
    li = hg.next()
    tkzr = li.create_tokenizer()
    assert tkzr.line_no == 2
    assert tkzr.start == 0
    assert tkzr.end == 10
    assert tkzr.line_content == "asdf ghjk "
    assert tkzr.source == source


def test_invalid_commentfiner() -> None:
    lines = """
asdf ghjk # QWEER
"""
    source = "test_create_tokenizer"
    with pytest.raises(HierGenInvalidCommentFinderError):
        _ = HierGen.from_line_with_newlines(
            lines,
            source_name=source,
            comment_finder=HashtagCommentFinder,  # type: ignore[arg-type]
        )


def test_exceptions_with_wrong_factory_types() -> None:
    with pytest.raises(HiergenInvalidLineSourceError):
        _ = HierGen.from_any(4)  # type: ignore[arg-type]
    with pytest.raises(HiergenInvalidLineSourceError):
        _ = HierGen.from_line_generator(4)  # type: ignore[arg-type]
    with pytest.raises(HiergenInvalidLineSourceError):
        _ = HierGen.from_line_list(4)  # type: ignore[arg-type]
    with pytest.raises(HiergenInvalidLineSourceError):
        _ = HierGen.from_line_with_newlines(4)  # type: ignore[arg-type]
    with pytest.raises(HiergenInvalidLineSourceError):
        _ = HierGen.from_text_file(4)  # type: ignore[arg-type]
