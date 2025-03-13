import pytest

from hiergen.exceptions import (
    CannotMatchNextTokenError,
    HiergenError,
    TokenizerAtEndError,
    TokenizerError,
    UnterminatedQuoteTokenError,
)

SOURCE = "TestSource"
LINE = "This is a line"
LINE_NO = 4
START = 3
END = 6


def test_TokenizerAtEndError() -> None:
    ex = TokenizerAtEndError(
        SOURCE,
        LINE,
        LINE_NO,
        START,
    )
    with pytest.raises(TokenizerAtEndError):
        raise ex
    assert ex.source == SOURCE
    assert ex.line == LINE
    assert ex.line_no == LINE_NO
    assert ex.start == START


def test_CannotMatchNextTokenError() -> None:
    ex = CannotMatchNextTokenError(
        SOURCE,
        LINE,
        LINE_NO,
        START,
    )
    with pytest.raises(CannotMatchNextTokenError):
        raise ex
    assert ex.source == SOURCE
    assert ex.line == LINE
    assert ex.line_no == LINE_NO
    assert ex.start == START


def test_HiergenError() -> None:
    ex = HiergenError
    with pytest.raises(HiergenError):
        raise ex


def test_TokenizerError() -> None:
    ex = TokenizerError(
        SOURCE,
        LINE,
        LINE_NO,
        START,
    )
    with pytest.raises(TokenizerError):
        raise ex
    assert ex.source == SOURCE
    assert ex.line == LINE
    assert ex.line_no == LINE_NO
    assert ex.start == START


def test_UnterminatedQuoteTokenError() -> None:
    ex = UnterminatedQuoteTokenError(
        SOURCE,
        LINE,
        LINE_NO,
        START,
    )
    with pytest.raises(UnterminatedQuoteTokenError):
        raise ex
    assert ex.source == SOURCE
    assert ex.line == LINE
    assert ex.line_no == LINE_NO
    assert ex.start == START
