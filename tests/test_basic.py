"""Tests for trawl package."""

import pytest

from trawl import __version__


def test_version():
    """Test that version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__.split(".")) >= 2


def test_import():
    """Test that main modules can be imported."""
    try:
        from trawl.cli import main
        from trawl.main import app
        from trawl.tui_app import SearchXApp
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import modules: {e}")


def test_config():
    """Test configuration loading."""
    from trawl.core.config import API_BASE, SEARXNG_BASE_URL
    # These should be loaded from environment or have defaults
    assert API_BASE is not None
    assert SEARXNG_BASE_URL is not None