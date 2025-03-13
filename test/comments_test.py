import pytest

from hiergen.comments import (
    HashtagCommentFinder,
    SemicolonCommentFinder,
    SlashSlashCommentFinder,
    _CommentFinder,
)


def test_HashtagCommentFinder() -> None:
    cf = HashtagCommentFinder()
    assert cf.find("asdf zxcv") == 9
    assert cf.find("asdf zxcv#") == 9
    assert cf.find("asdf #zxcv") == 5
    assert cf.find("#asdf #zxcv") == 0
    assert cf.find('asdf "#zx\\"cv#"') == 15


def test_SemicolonCommentFinder() -> None:
    cf = SemicolonCommentFinder()
    assert cf.find("asdf zxcv") == 9
    assert cf.find("asdf zxcv;") == 9
    assert cf.find("asdf ;zxcv") == 5
    assert cf.find(";asdf ;zxcv") == 0
    assert cf.find('asdf ";zx\\"cv;"') == 15


def test_SlashSlashCommentFinder() -> None:
    cf = SlashSlashCommentFinder()
    assert cf.find("asdf zxcv") == 9
    assert cf.find("asdf zxcv//") == 9
    assert cf.find("asdf //zxcv") == 5
    assert cf.find("//asdf //zxcv") == 0
    assert cf.find('asdf "//zx\\"cv//"') == 17
    assert cf.find("asdf / zxcv") == 11
    assert cf.find("asdf / zxcv //") == 12


def test_base_find() -> None:
    cf = _CommentFinder()
    with pytest.raises(NotImplementedError):
        cf.find("asdf")
