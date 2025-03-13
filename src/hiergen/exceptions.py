"""Exceptions related to the HierGen package.

These are the exceptions that might be raised by the HierGen
package modules. They all derive from HiergenError which is
derived from Exception.

Copyright 2024 Mark Hamann
Licensed under MIT license. See LICENSE.
"""

from typing import Any


class HiergenError(Exception):
    """Base class for exceptions in this package.

    This is the only exception in this package that derived from Exception.
    """

    def __init__(self, *args: list[Any]) -> None:
        """Create an exception from this package.

        Args:
            args (list): Native base class arguments

        """
        super().__init__(*args)


class HiergenProcessingError(HiergenError):
    """Base class for processing errors where source and line number are known."""

    def __init__(self, source: str, line_no: int, *args: list[Any]) -> None:
        """Create a processing exception.

        Args:
            source (str): A text description of the line source.
            line_no (int): The line number.
            args (list): Native base class arguments

        """
        super().__init__(*args)
        self._source = source
        self._line_no = line_no

    @property
    def source(self) -> str:
        """Get a string representation of the source of the data.

        This can be passes as `source_name` to the factory methods
        and in the case of using a text_file defaults to the
        name of the file.

        Returns:
            str: The name of the source.

        """
        return self._source

    @property
    def line_no(self) -> int:
        """Get the line number of the line.

        The line number is 1-based.  With `source` the location
        of an error can be used to point to an exact line where
        a problem occurred.

        Returns:
            int: Index of the line (1 based)

        """
        return self._line_no


class HierGenInvalidCommentFinderError(HiergenError):
    """The factory method did not receive a valid `comment_finder`."""

    def __init__(self, *args: list[Any]) -> None:
        """Create an exception when the user sends an invalid comment_finder.

        Args:
            args (list): Base class arguments

        """
        super().__init__(*args)


class HiergenInvalidLineSourceError(HiergenError):
    """The factory method did not receive a valid line source."""

    def __init__(self, type_name: str, *args: list[Any]) -> None:
        """Create an exception to indicate that the line source is not valid.

        Args:
            type_name (str): The actual type anem of the line source.
            args (list): Base class arguments

        """
        super().__init__(*args)
        self._type_name = type_name

    def __str__(self) -> str:
        return f"Cannot use line source of type {self._type_name}"


class TokenizerError(HiergenProcessingError):
    """The tokenizer has encountered an error."""

    def __init__(self, source: str, line: str, line_no: int, start: int, *args: list[Any]) -> None:
        """Create an exception when the tokenizer encounters an error.

        Args:
            source (str): Name of the source of the lines.
            line (str): The actual line where the error occurred.
            line_no (int): The 1 based line number where the error occurred.
            start (int): The 0 based character cursor when the error occurred.
            args (list): Base class arguments

        """
        super().__init__(source, line_no, *args)
        self._line = line
        self._start = start

    @property
    def line(self) -> str:
        """Get the actual line where the problem occurred.

        Returns:
            str: The line.

        """
        return self._line

    @property
    def start(self) -> int:
        """Get the 0 based character index when the error occurred.

        Returns:
            int: 0 based index in `line`

        """
        return self._start


class UnterminatedQuoteTokenError(TokenizerError):
    """The tokenizer located a start quote but no matching endquote."""

    def __init__(self, source: str, line: str, line_no: int, start: int, *args: list[Any]) -> None:
        """Create an exception to indicate that an end quote was not located.

        Args:
            source (str): Name of the source of the lines.
            line (str): The actual line where the error occurred.
            line_no (int): The 1 based line number where the error occurred.
            start (int): The 0 based character cursor when the error occurred.
            args (list): Base class arguments

        """
        super().__init__(source, line, line_no, start, *args)


class CannotMatchNextTokenError(TokenizerError):
    """The requested asked for a specific token type but it cannot be found."""

    def __init__(self, source: str, line: str, line_no: int, start: int, *args: list[Any]) -> None:
        """Create an exception is untokenized content remain but not of the requested `token_type`.

        Args:
            source (str): Name of the source of the lines.
            line (str): The actual line where the error occurred.
            line_no (int): The 1 based line number where the error occurred.
            start (int): The 0 based character cursor when the error occurred.
            args (list): Base class arguments

        """
        super().__init__(source, line, line_no, start, *args)


class TokenizerAtEndError(TokenizerError):
    """The Tokenizer has no more tokens to process.

    The cursor is either at the end of the line or at the start of
    a comment. In `__next__(self)` this is rereaised as StopIterationError.
    """

    def __init__(self, source: str, line: str, line_no: int, start: int, *args: list[Any]) -> None:
        """Create an exception to indicate that there is no more content to process.

        Args:
            source (str): Name of the source of the lines.
            line (str): The actual line where the error occurred.
            line_no (int): The 1 based line number where the error occurred.
            start (int): The 0 based character cursor when the error occurred.
            args (list): Base class arguments

        """
        super().__init__(source, line, line_no, start, *args)
