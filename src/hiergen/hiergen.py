"""The hierarchical generator.

Copyright 2024 Mark Hamann
Licensed under MIT license. See LICENSE.
"""

from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator
from pathlib import Path

from hiergen.comments import _CommentFinder
from hiergen.exceptions import (
    HierGenInvalidCommentFinderError,
    HiergenInvalidLineSourceError,
)
from hiergen.tokenizer import Tokenizer

type LineGenerator = Generator[tuple[str, int]]

_NO_SOURCE = "No source"


class LineInfo:
    """LineInfo is the object yielded by HierGen.

    It contains information about the line needed to:
        * get at the contents
        * create clickable error messages
        * iterate over the children of the current line
    """

    def __init__(
        self,
        line: str,
        source: str,
        line_no: int,
        start: int,
        end: int,
        children: HierGen | None = None,
    ) -> None:
        """Information about a single line.

        Args:
            line (str): The text of the line
            source (str): The source of the line
            line_no (int): _description_
            start (int): _description_
            end (int): _description_
            children (HierGen | None, optional): _description_. Defaults to None.

        """
        self._line = line
        self._source = source
        self._line_no = line_no
        self._start = start
        self._end = end
        self._children = children

    @property
    def line(self) -> str:
        """Get the line including indent and comments.

        Returns:
            str: The entire line

        """
        return self._line

    @property
    def source(self) -> str:
        """Get the line source.

        Returns:
            str: The source of the line

        """
        return self._source

    @property
    def line_no(self) -> int:
        """Get the line number of the line (1-based).

        Returns:
            int: The line number

        """
        return self._line_no

    @property
    def start(self) -> int:
        """Get the first non-indent character index.

        Returns:
            int: Index of the first character

        """
        return self._start

    @property
    def end(self) -> int:
        """Get the first comment character index or EOL.

        Returns:
            int: Index of the first non-content character

        """
        return self._end

    @property
    def content(self) -> str:
        """Get the portion of the line not including indents or comments.

        Returns:
            str: The content portion of the line

        """
        return self.line[self.start : self.end]

    @property
    def children(self) -> HierGen:
        """Get the children line iterator.

        Returns:
            HierGen: An iterator with children

        """
        return self._children  # type: ignore  # noqa: PGH003

    @children.setter
    def children(self, children: HierGen) -> None:
        """Set the child nodes. If already set, raises an error.

        Args:
            children (HierGen): Direct children of the line.

        """
        self._children = children

    def create_tokenizer(self) -> Tokenizer:
        """Create a Tokenizer based on the current line.

        Returns:
            Tokenizer: A new tokenizer.

        """
        return Tokenizer(self.source, self.line, self.line_no, self.start, self.end)


class HierGen:
    """HierGen is a generator that iterates over a set of indented lines.

    It yields all of the lines at that indentation level until there is
    a line that is less indented. The LineInfo that it yields also contains
    a HierGen that contains the next indentation level whose lines are
    the direct children. These also yield the LineInfo at that level along
    with the grandchildren.
    """

    class _Internal:
        def __init__(
            self,
            *,
            line_generator: LineGenerator,
            comment_finder: _CommentFinder | None = None,
            peeked: LineInfo | None = None,
            source_name: str | None = None,
        ) -> None:
            self.line_generator = line_generator
            if comment_finder and not isinstance(comment_finder, _CommentFinder):
                raise HierGenInvalidCommentFinderError
            self.comment_finder = comment_finder
            self.peeked = peeked
            self.source_name = source_name if source_name else _NO_SOURCE

    @staticmethod
    def from_any(
        source: str | list[str] | Path | LineGenerator,
        *,
        comment_finder: _CommentFinder | None = None,
        source_name: str | None = None,
    ) -> HierGen:
        """Generate a top-level `HierGen` from any valid source.

        Args:
            source (str | list[str] | Path | LineGenerator): The source of the lines to process.
            comment_finder (_CommentFinder | None, optional): A CommentFinder. Defaults to None.
            source_name (str | None, optional): Text description of a source. Defaults to None.

        Raises:
            HiergenInvalidLineSourceError: The `source` is not a valid source of lines.

        Returns:
            HierGen: A top-level `HierGen`.

        """
        if isinstance(source, str):
            return HierGen.from_line_with_newlines(
                source, comment_finder=comment_finder, source_name=source_name
            )
        if isinstance(source, list):
            return HierGen.from_line_list(
                source, comment_finder=comment_finder, source_name=source_name
            )
        if isinstance(source, Path):
            return HierGen.from_text_file(
                source, comment_finder=comment_finder, source_name=source_name
            )
        if isinstance(source, Generator):
            return HierGen.from_line_generator(
                source, comment_finder=comment_finder, source_name=source_name
            )
        raise HiergenInvalidLineSourceError(str(type(source)))

    @staticmethod
    def from_line_generator(
        line_generator: LineGenerator,
        *,
        comment_finder: _CommentFinder | None = None,
        source_name: str | None = None,
    ) -> HierGen:
        """Generate a top-level `HierGen` from any valid source.

        Args:
            line_generator (LineGenerator): A generator that produces the lines to process
                and their line number.
            comment_finder (_CommentFinder | None, optional): A CommentFinder. Defaults to None.
            source_name (str | None, optional): Text description of a source. Defaults to None.

        Raises:
            HiergenInvalidLineSourceError: The `source` is not a valid source of lines.

        Returns:
            HierGen: A top-level `HierGen`.

        """
        if not isinstance(line_generator, Iterable):
            raise HiergenInvalidLineSourceError(str(type(line_generator)))
        hg_internal = HierGen._Internal(
            line_generator=line_generator,
            comment_finder=comment_finder,
            source_name=source_name if source_name else "LineGenerator",
        )
        return HierGen(0, hg_internal)

    @staticmethod
    def from_line_with_newlines(
        lines: str,
        *,
        comment_finder: _CommentFinder | None = None,
        source_name: str | None = None,
    ) -> HierGen:
        """Generate a top-level `HierGen` from a single string with newline-separated lines.

        Args:
            lines (str): A single string with newline-separated lines to process.
            comment_finder (_CommentFinder | None, optional): A CommentFinder. Defaults to None.
            source_name (str | None, optional): Text description of a source. Defaults to None.

        Raises:
            HiergenInvalidLineSourceError: The `source` is not a valid source of lines.

        Returns:
            HierGen: A top-level `HierGen`.

        """
        if not isinstance(lines, str):
            raise HiergenInvalidLineSourceError(str(type(lines)))

        def line_gen(lines: str) -> LineGenerator:
            cursor = 0
            end = len(lines)
            line_no = 0
            while cursor < end:
                line_end = lines.find("\n", cursor, end)
                if line_end >= 0:
                    line = lines[cursor:line_end]
                    cursor = line_end + 1
                else:
                    line = lines[cursor:end]
                    cursor = end
                line_no += 1
                yield line, line_no

        return HierGen.from_line_generator(
            line_gen(lines),
            comment_finder=comment_finder,
            source_name=source_name if source_name else "SingleLine",
        )

    @staticmethod
    def from_line_list(
        lines: list[str],
        *,
        comment_finder: _CommentFinder | None = None,
        source_name: str | None = None,
    ) -> HierGen:
        """Generate a top-level `HierGen` from a list of str lines.

        Args:
            lines (list[str]): A list of lines to process.
            comment_finder (_CommentFinder | None, optional): A CommentFinder. Defaults to None.
            source_name (str | None, optional): Text description of a source. Defaults to None.

        Raises:
            HiergenInvalidLineSourceError: The `source` is not a valid source of lines.

        Returns:
            HierGen: A top-level `HierGen`.

        """
        if not isinstance(lines, list):
            raise HiergenInvalidLineSourceError(str(type(lines)))

        def line_gen(lines: list[str]) -> LineGenerator:
            for line_no, line in enumerate(lines, start=1):
                yield line, line_no

        return HierGen.from_line_generator(
            line_gen(lines),
            comment_finder=comment_finder,
            source_name=source_name if source_name else "LineList",
        )

    @staticmethod
    def from_text_file(
        text_file: Path,
        *,
        comment_finder: _CommentFinder | None = None,
        source_name: str | None = None,
    ) -> HierGen:
        """Generate a top-level `HierGen` from a list of str lines.

        Args:
            text_file (Path): A file of lines to process.
            comment_finder (_CommentFinder | None, optional): A CommentFinder. Defaults to None.
            source_name (str | None, optional): Text description of a source. Defaults to None.

        Raises:
            HiergenInvalidLineSourceError: The `source` is not a valid source of lines.

        Returns:
            HierGen: A top-level `HierGen`.

        """
        if not isinstance(text_file, Path):
            raise HiergenInvalidLineSourceError(str(type(text_file)))

        def line_gen(text_file: Path) -> LineGenerator:
            line_no = 0
            with text_file.open() as f:
                while True:
                    line = f.readline()
                    if len(line) == 0:
                        break
                    line_no += 1
                    yield line[0:-1], line_no

        if source_name is None:
            source_name = str(text_file.resolve())

        return HierGen.from_line_generator(
            line_gen(text_file),
            comment_finder=comment_finder,
            source_name=source_name,
        )

    @staticmethod
    def _leading_whitespace_length(line: str) -> int:
        """Get the number of leading spaces in `line`.

        Args:
            line (str): A single line

        Returns:
            int: The number of leading spaces.

        """
        for i, c in enumerate(line):
            if c != " ":
                return i
        return 0

    def __init__(self, indent: int, internal: HierGen._Internal) -> None:
        """Instantiate a hierarchical generator.

        Used to iterate over lines that use indentation to express hierarchy.

        Args:
            indent (int): The level of indentation of the lines to yield
            internal (HierGen._Internal): Internal info. Use factory
                methods for the top level generator.

        Raises:
            HiergenInvalidLineSourceError: The line source is not an iterable that delivers lines
            StopIteration: No more lines to iterate at this level

        Yields:
            LineInfo: Information about the line at the current level. Includes a
            `HierGen` for its children.

        """
        self._indent = indent
        self._internal = internal
        self._peeked: LineInfo | None = None
        self._is_empty = False

    def __iter__(self) -> Iterator[LineInfo]:
        """Return an iterator over the source.

        Returns:
            Iterator[LineInfo]: The iterator

        """
        return self

    def __next__(self) -> LineInfo:
        """Get the next LineInfo.

        Returns:
            LineInfo: Information about the line.

        Raises:  # noqa: DOC502
            StopIteration: Raised when ther are no more lines.

        """
        return self.next()

    def _get_next_line(self) -> LineInfo:
        """Get the next line that has content.

        Skips any lines that are only white space or are comments

        Returns:
            LineInfo: information about the line

        Raises:
            StopIteration: if there are no lines left

        """
        while True:
            line, line_no = next(self._internal.line_generator)
            start = HierGen._leading_whitespace_length(line)
            if self._internal.comment_finder is not None:
                end = self._internal.comment_finder.find(line, start)
            else:
                end = len(line)
            li = LineInfo(line, self.source, line_no, start, end)
            if end > start and not li.content.isspace():
                return li

    def peek(self) -> LineInfo:
        """Get the next LineInfo if there is one.

        Returns:
            LineInfo: The next line

        Raises:
            StopIteration: No more lines exist

        """
        if self._internal.peeked is None:
            self._internal.peeked = self._get_next_line()
        return self._internal.peeked

    def next(self) -> LineInfo:
        """Get the next LineInfo at the current level.

        Raises:
            StopIteration: No more tokens

        Returns:
            LineInfo: Information about the line

        """
        # Empty iterator--stop immediately
        if self.is_empty:
            raise StopIteration

        while True:
            # If there is a peeked line, return it
            if li := self._internal.peeked:
                self._internal.peeked = None
            else:
                # Get next line or raise StopItertion
                li = self._get_next_line()

            # See if the line is at our level
            if li.start == self._indent:
                # Assume no children unless peek reveals a line with
                # more indentation
                child_hg = None

                try:
                    peeked = self.peek()

                    # There is a next line--get its indentation
                    if peeked is not None and peeked.start > self._indent:
                        # It's further indented so starts children
                        child_hg = HierGen(peeked.start, self._internal)

                except StopIteration:
                    # No lines left to process--hence no children
                    pass

                if child_hg is None:
                    child_hg = HierGen(0, self._internal)
                    child_hg._is_empty = True  # noqa: SLF001

                li.children = child_hg
                return li

            # Check if we're done because the next line is an uncle
            if li.start < self._indent:
                self._internal.peeked = li

                # Done with this depth of iteration
                raise StopIteration

            # if we got here we're on an unconsumed child--skip it
            # by going back to the top of the while loop

    @property
    def source(self) -> str:
        """Get the string representation of the line source.

        Returns:
            str: A string representing the source.

        """
        return self._internal.source_name

    @property
    def is_empty(self) -> bool:
        """Determine if the iterator is empty before starting.

        Returns:
            bool: True if the iterator was always empty

        """
        return self._is_empty
