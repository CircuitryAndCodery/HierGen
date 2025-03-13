"""A collection of various comment finders.

A comment finder is an object that has a find(str, int) -> int method
that looks for evidence of an inline comment. It returns either the
index of the first comment character or the length of the line if there
is no comment.

Copyright 2024 Mark Hamann
Licensed under MIT license. See LICENSE.
"""

from typing import override


class _CommentFinder:
    """Base class for comment finders.

    CommentFinders all derive from this class which only has a
    `find(self, line: str, start: int = 0) -> int` method
    """

    def find(self, line: str, start: int = 0) -> int:
        del line
        del start
        raise NotImplementedError


class HashtagCommentFinder(_CommentFinder):
    """Find index of # comment in a line.

    The comment finder honors strings in ' or ".
    """

    @override
    def find(self, line: str, start: int = 0) -> int:
        """Find the index of the # that starts a comment.

        If there is no comment, returns the `len(line)`.
        Honors strings in " and `.

        Args:
            line (str): A line that may have a comment
            start (int, optional): Index to start looking from.
                Defaults to 0.

        Returns:
            int: Index of the comment or end of line

        """
        quote = None
        escape = False
        i = -1
        for i, c in enumerate(line[start:], start=start):
            if quote is not None:
                if escape:
                    escape = False
                elif c == quote:
                    quote = None
                elif c == "\\":
                    escape = True

            elif c in ['"', "'"]:
                quote = c

            elif c == "#":
                return i
        return i + 1


class SemicolonCommentFinder(_CommentFinder):
    """Find index of ; comment in a line.

    The comment finder honors strings in ' or ".
    """

    @override
    def find(self, line: str, start: int = 0) -> int:
        """Find the index of the ; that starts a comment.

        If there is no comment, returns the `len(line)`.
        Honors strings in " and `.

        Args:
            line (str): A line that may have a comment
            start (int, optional): Index to start looking from.
                Defaults to 0.

        Returns:
            int: Index of the comment or end of line

        """
        quote = None
        escape = False
        for i, c in enumerate(line[start:], start=start):
            if quote is not None:
                if escape:
                    escape = False
                elif c == quote:
                    quote = None
                elif c == "\\":
                    escape = True

            elif c in ['"', "'"]:
                quote = c

            elif c == ";":
                return i
        return i + 1


class SlashSlashCommentFinder(_CommentFinder):
    """Find index of // comment in a line.

    The comment finder honors strings in ' or ".
    """

    @override
    def find(self, line: str, start: int = 0) -> int:
        """Find the index of the // that starts a comment.

        If there is no comment, returns the `len(line)`.
        Honors strings in " and `.

        Args:
            line (str): A line that may have a comment
            start (int, optional): Index to start looking from.
                Defaults to 0.

        Returns:
            int: Index of the comment or end of line

        """
        quote = None
        escape = False
        first_check = -1
        for i, c in enumerate(line[start:], start=start):
            if first_check >= 0:
                if c == "/":
                    return first_check
                first_check = -1

            if quote is not None:
                if escape:
                    escape = False
                elif c == quote:
                    quote = None
                elif c == "\\":
                    escape = True

            elif c in ['"', "'"]:
                quote = c

            elif c == "/":
                first_check = i
        return i + 1
