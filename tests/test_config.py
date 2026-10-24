import pytest

from src.config import Settings, _get_int


def test_invalid_integer_configuration_fails_clearly(monkeypatch):
    monkeypatch.setenv("RAG_TOP_K", "many")
    with pytest.raises(ValueError, match="RAG_TOP_K must be an integer"):
        _get_int("RAG_TOP_K", 5)


def test_settings_validate_chunk_windows_and_index_name():
    with pytest.raises(ValueError, match="CHUNK_OVERLAP_CHARS"):
        Settings(chunk_size_chars=20, chunk_overlap_chars=20)
    with pytest.raises(ValueError, match="INDEX_NAME"):
        Settings(index_name="../outside")

