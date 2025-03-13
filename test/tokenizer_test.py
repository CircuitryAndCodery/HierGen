import pytest

from hiergen.exceptions import (
    CannotMatchNextTokenError,
    TokenizerAtEndError,
    UnterminatedQuoteTokenError,
)
from hiergen.tokenizer import Tokenizer, TokenType

SOURCE = "source"
LINE_NO = 0


def test_empty_str() -> None:
    tt = Tokenizer(SOURCE, "", LINE_NO)
    assert tt.is_at_end


def test_get_words() -> None:
    txt = "asdf zxcv"
    tt = Tokenizer(SOURCE, txt, LINE_NO)
    assert not tt.is_at_end
    assert tt.next() == "asdf"
    assert tt.next(TokenType.Normal) == "zxcv"
    assert tt.is_at_end


def test_indented() -> None:
    txt = "    asdf zxcv"
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert not tt.is_at_end
    assert tt.next(TokenType.Normal) == "asdf"
    assert tt.next() == "zxcv"
    assert tt.is_at_end
    with pytest.raises(TokenizerAtEndError):
        tt.next()
    with pytest.raises(TokenizerAtEndError):
        tt.next(TokenType.Normal)


def test_get_double_quoted() -> None:
    txt = r"""
    "asdf" "zxcv"
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert not tt.is_at_end
    assert tt.next(TokenType.DoubleQuote) == "asdf"
    assert tt.next() == "zxcv"
    assert tt.is_at_end
    with pytest.raises(TokenizerAtEndError):
        tt.next()
    with pytest.raises(TokenizerAtEndError):
        tt.next(TokenType.DoubleQuote)


def test_get_double_quoted_escapes() -> None:
    txt = r"""
    "as\"df" "zx\"cv"
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert not tt.is_at_end
    assert tt.next() == 'as"df'
    assert tt.next() == 'zx"cv'
    assert tt.is_at_end
    with pytest.raises(TokenizerAtEndError):
        tt.next()
    with pytest.raises(TokenizerAtEndError):
        tt.next(TokenType.DoubleQuote)


def test_get_double_quoted_escapes_escaped() -> None:
    txt = r"""
    "as\"df" "zx\"cv"
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert not tt.is_at_end
    assert tt.next() == 'as"df'
    assert tt.next() == 'zx"cv'
    assert tt.is_at_end
    with pytest.raises(TokenizerAtEndError):
        tt.next()
    with pytest.raises(TokenizerAtEndError):
        tt.next(TokenType.DoubleQuote)


def test_is_at_end_both() -> None:
    txt = "asdf "
    tt = Tokenizer(SOURCE, txt, LINE_NO)
    assert tt.next() == "asdf"
    assert tt.is_at_end


def test_set_end() -> None:
    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4, end=8)
    assert tt.next() == "asdf"
    assert tt.is_at_end


def test_set_end_trailing_ws() -> None:
    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4, end=9)
    assert tt.next() == "asdf"
    assert tt.is_at_end


def test_line_from_cursor() -> None:
    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4, end=9)
    assert tt.remaining == "asdf "

    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, start=4, end=8)
    assert tt.remaining == "asdf"


def test_char_at_cursor() -> None:
    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=3, end=9)
    assert tt.char_at_cursor == "a"
    assert tt.next() == "asdf"
    assert tt.is_at_end


def test_get() -> None:
    txt = r"""
    asdf "zx\"cv"
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert tt.next() == "asdf"
    assert tt.next() == 'zx"cv'


def test_quoted_errors() -> None:
    txt = '"asdf'
    tt = Tokenizer(SOURCE, txt, LINE_NO)
    with pytest.raises(UnterminatedQuoteTokenError):
        tt.next()

    txt = "'asdf"
    tt = Tokenizer(SOURCE, txt, LINE_NO)
    with pytest.raises(UnterminatedQuoteTokenError):
        tt.next()


def test_tokenizer_as_iterator() -> None:
    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, LINE_NO)
    tk_list = list(tt)
    assert tk_list[0] == "asdf"
    assert tk_list[1] == "zxcv"


def test_source() -> None:
    tt = Tokenizer("asdf", "1234", 13)
    assert tt.source == "asdf"


def test_line_no() -> None:
    tt = Tokenizer("asdf", "1234", 13)
    assert tt.line_no == 13


def test_line_content() -> None:
    tt = Tokenizer("asdf", "    1234    ", 13, 4, 8)
    assert tt.line_content == "1234"


def test_get_single_quoted() -> None:
    txt = r"""
    'asdf' 'zxcv'
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert not tt.is_at_end
    assert tt.next(TokenType.SingleQuote) == "asdf"
    assert tt.next() == "zxcv"
    assert tt.is_at_end
    with pytest.raises(TokenizerAtEndError):
        tt.next()
    with pytest.raises(TokenizerAtEndError):
        tt.next(TokenType.SingleQuote)


def test_get_single_quoted_escapes() -> None:
    txt = r"""
    'as\'df' 'zx\'cv'
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert not tt.is_at_end
    assert tt.next() == "as'df"
    assert tt.next() == "zx'cv"
    assert tt.is_at_end
    with pytest.raises(TokenizerAtEndError):
        tt.next()
    with pytest.raises(TokenizerAtEndError):
        tt.next(TokenType.SingleQuote)


def test_get_single_quoted_escapes_escaped() -> None:
    txt = r"""
    'as\'df' 'zx\'cv'
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert not tt.is_at_end
    assert tt.next() == "as'df"
    assert tt.next() == "zx'cv"
    assert tt.is_at_end
    with pytest.raises(TokenizerAtEndError):
        tt.next()
    with pytest.raises(TokenizerAtEndError):
        tt.next(TokenType.DoubleQuote)


def test_single_quoted_raw() -> None:
    txt = r"""
    'as\'df' 'zx\'cv'
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    unescaped = tt.next(token_type=TokenType.SingleQuote | TokenType.Raw)
    assert unescaped == "as\\'df"


def test_double_quoted_raw() -> None:
    txt = r"""
    "as\"df" "zx\"cv"
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    unescaped = tt.next(token_type=TokenType.DoubleQuote | TokenType.Raw)
    assert unescaped == 'as\\"df'


def test_cannot_match_token() -> None:
    txt = r"""
    'as\'df' 'zx\'cv'
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    with pytest.raises(CannotMatchNextTokenError):
        _ = tt.next(token_type=TokenType.Normal)


def test_set_line_no() -> None:
    txt = r"""
    'as\'df' 'zx\'cv'
""".splitlines()[1]
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert tt.line_no == LINE_NO
    tt.line_no = LINE_NO + 1
    assert tt.line_no == LINE_NO + 1


def test_cannot_match_next() -> None:
    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    assert tt.next() == "asdf"
    with pytest.raises(CannotMatchNextTokenError):
        tt.next(token_type=0)  # type: ignore[arg-type]


def test_peek() -> None:
    txt = "    asdf zxcv "
    tt = Tokenizer(SOURCE, txt, LINE_NO, start=4)
    peeked1 = tt.peek()
    assert peeked1 == "asdf"
    peeked2 = tt.peek()
    assert peeked2 == "asdf"
    next1 = tt.next()
    assert next1 == "asdf"
    peeked3 = tt.peek()
    assert peeked3 == "zxcv"
    next2 = tt.next()
    assert next2 == "zxcv"
    peeked4 = tt.peek()
    assert peeked4 is None


# def test_() -> None:
