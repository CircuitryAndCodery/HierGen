"""A tokenizer class that takes a line and returns string tokens.

Copyright 2024 Mark Hamann
Licensed under MIT license. See LICENSE.
"""

from ast import literal_eval
from collections.abc import Iterator
from enum import IntFlag

from hiergen.exceptions import (
    CannotMatchNextTokenError,
    TokenizerAtEndError,
    UnterminatedQuoteTokenError,
)


class TokenType(IntFlag):
    """Flags to direct token matching.

    Attributes:
        Normal (IntFlag):
        SingleQuote (IntFlag):
        DoubleQuote (IntFlag):
        Raw (IntFlag):
        Unquoted (IntFlag):

    """

    Normal = 0x01
    """Match tokens up to next whitespace character
    """

    SingleQuote = 0x02
    """Match a single quoted string taking escaped characters into account
    """

    DoubleQuote = 0x04
    """Match a double quoted string taking escaped characters into account
    """

    Raw = 0x10
    """Return unescaped strings when matching SingleQuote or DoubleQuote
    """

    Unquoted = 0x20


ALL_TOKENS = TokenType.Normal | TokenType.SingleQuote | TokenType.DoubleQuote
"""Default matching strategy. Matches all token types
"""


class Tokenizer:
    """Tokenizer takes a single line and incrementally scans for tokens.

    Use the Tokenizer to take a line and extract tokens as desires. It contains
    enough information about the source of the line to create an appropriate
    clickable problem report.

    """

    def __init__(
        self,
        source: str,
        line: str,
        line_no: int = -1,
        start: int = -1,
        end: int = -1,
    ) -> None:
        """Tokenizer takes a single line and incrementally scans for tokens.

        Args:
            source (str): The source of the data
            line (str): The line being processed
            line_no (int, optional): The line number. Defaults to -1.
            start (int, optional): The index of the first content character. Defaults to -1.
            end (int, optional): The index of the first non-content character. Defaults to -1.

        """
        self._source = source
        self._line = line
        self._line_no = line_no
        self._start = max(start, 0)
        self._end = end if end >= 0 else len(line)
        self._cursor = self.start
        self._peek_ahead: tuple[int, int] = (-1, -1)

        # Skip passed any initital whitespace (typically there isn't any)
        self._eat_whitespace()

    def __iter__(self) -> Iterator[str]:
        """Get the iterator.

        Returns:
            Iterator[str]: An iterator that returns strings

        Yields:
            None

        """
        return self

    def __next__(self) -> str:
        """Get the next token.

        Raises:
            StopIteration: No more tokens.

        Returns:
            str: A string of the token.

        """
        try:
            return self.next()
        except TokenizerAtEndError:
            raise StopIteration from None

    def _eat_whitespace(self) -> None:
        """Advance cursor to the next non-whitespace character or end of line."""
        while self.cursor < self.end and self._line[self.cursor].isspace():
            self.cursor += 1

    def _find_end_of_normal(self) -> int:
        """Find first whitespace (or end of line) from cursor.

        Note:
            Does not update the cursor.

        Returns:
            int: index of the end of non-whitespace

        """
        track = self.cursor
        while track < self.end and not self._line[track].isspace():
            track += 1
        return track

    def _find_end_of_quoted(self) -> int:
        r"""Find the next quote character.

        The character must match the character at the cursor location.
        The backslash (\) is used to escape the next character.

        Note:
            Does not update the cursor.

        Raises:
            UnterminatedQuoteTokenError: Raised if the closing quote is missing

        Returns:
            int: index of the character after the matching quote

        """
        track = self.cursor + 1
        quote = self.whole_line[self.cursor]
        escaping = False
        while track < self.end:
            c = self._line[track]
            if escaping:
                escaping = False
            elif c == "\\":
                escaping = True
            elif c == quote:
                return track + 1
            track += 1
        raise UnterminatedQuoteTokenError(
            self.source,
            self.whole_line,
            self.line_no,
            self.start,
        )

    def _escaped(self, content: str) -> str:
        """Return an escaped string.

        Args:
            content (str): The string to escape

        Returns:
            str: An escaped string.

        """
        return literal_eval(f'"{content}"')

    @property
    def cursor(self) -> int:
        """Location in the line of the current character.

        Returns:
            int: An index in the line.

        """
        return self._cursor

    @cursor.setter
    def cursor(self, new_cursor: int) -> None:
        """Update the cursor location.

        Args:
            new_cursor (int): The new cursor location.

        """
        self._cursor = new_cursor

    @property
    def source(self) -> str:
        """Get the text representation of the line source.

        Returns:
            str: The name of the source.

        """
        return self._source

    @property
    def line_no(self) -> int:
        """The line number of the line.

        Returns:
            int: The line number.

        """
        return self._line_no

    @line_no.setter
    def line_no(self, new_line_no: int) -> None:
        """Update the line number.

        Args:
            new_line_no (int): The new line number

        """
        self._line_no = new_line_no

    @property
    def whole_line(self) -> str:
        """Get the whole line including indent and comment.

        Returns:
            str: The entire line

        """
        return self._line

    @property
    def line_content(self) -> str:
        """Get the part of the line without the indent and comment.

        Returns:
            str: The content part of the line

        """
        return self._line[self.start : self.end]

    @property
    def start(self) -> int:
        """Get the index of the first non-indent character.

        Returns:
            int: Index of the first non-indent character

        """
        return self._start

    @property
    def end(self) -> int:
        """Get the index of the first post-content character.

        Returns:
            int: Index of the first post-content character

        """
        return self._end

    @property
    def remaining(self) -> str:
        """Get the content from the cursor to the end of the content.

        Returns:
            str: Unconsumed content

        """
        return self.whole_line[self.cursor : self.end]

    @property
    def is_at_end(self) -> bool:
        """Return True if there are no more tokens.

        Returns:
            bool: True - no more tokens. False - more content

        """
        if self.cursor >= self.end:
            return True
        return self.remaining.isspace()

    @property
    def char_at_cursor(self) -> str:
        """Get the character at the cursor. "" if at end.

        Returns:
            str: A character or ""

        """
        return "" if self.cursor >= self.end else self.whole_line[self.cursor]

    def _peek(self, token_type: TokenType = ALL_TOKENS) -> tuple[str, int]:
        if self.is_at_end:
            raise TokenizerAtEndError(
                self.source,
                self.whole_line,
                self.line_no,
                self.start,
            )

        c = self.char_at_cursor
        if c == "'":
            if token_type & TokenType.SingleQuote:
                start = self.cursor
                end = self._find_end_of_quoted()
                content = self.whole_line[start + 1 : end - 1]
                self._eat_whitespace()
                if token_type & TokenType.Raw:
                    return content, end
                return self._escaped(content), end
            raise CannotMatchNextTokenError(
                self.source,
                self.whole_line,
                self.line_no,
                self.start,
            )
        if c == '"':
            if token_type & TokenType.DoubleQuote:
                start = self.cursor
                end = self._find_end_of_quoted()
                content = self.whole_line[start + 1 : end - 1]
                if token_type & TokenType.Raw:
                    return content, end
                return self._escaped(content), end
        elif token_type & TokenType.Normal:
            start = self.cursor
            end = self._find_end_of_normal()
            return self.whole_line[start:end], end
        raise CannotMatchNextTokenError(
            self.source,
            self.whole_line,
            self.line_no,
            self.start,
        )

    def peek(self, token_type: TokenType = ALL_TOKENS) -> str | None:
        """Peek at the next token that uses token_type.

        Args:
            token_type (TokenType, optional): The token type to look for.
                Defaults to ALL_TOKENS.

        Returns:
            str | None: The next token, unconsumed or None if at end

        """
        try:
            content, _ = self._peek(token_type)
        except TokenizerAtEndError:
            return None
        return content

    def next(self, token_type: TokenType = ALL_TOKENS) -> str:
        """Get the next string of `token_type`.

        Args:
            token_type (TokenType, optional): The type of token to find.
                Defaults to ALL_TOKENS.

        Raises:
            TokenizerAtEndError: At end. No more tokens.
            CannotMatchNextTokenError: No match available, but not at end

        Returns:
            str: A token that matches the `token_type`

        """
        content, end = self._peek(token_type)
        self._cursor = end
        self._eat_whitespace()
        return content
