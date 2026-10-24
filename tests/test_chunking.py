import pytest

from src.chunking import chunk_text


def test_chunk_text_preserves_overlap_and_covers_input():
    assert chunk_text("abcdefghij", size=4, overlap=1) == ["abcd", "defg", "ghij"]


def test_chunk_text_handles_empty_and_whitespace():
    assert chunk_text("  \n ", size=4, overlap=1) == []


@pytest.mark.parametrize(("size", "overlap"), [(0, 0), (-1, 0), (4, -1), (4, 4)])
def test_chunk_text_rejects_invalid_window(size, overlap):
    with pytest.raises(ValueError):
        chunk_text("some text", size=size, overlap=overlap)

