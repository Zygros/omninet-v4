"""Regression checks for the installable OmniNet distribution metadata."""

from importlib.metadata import version

from omninet import __version__


def test_installed_distribution_matches_runtime_version():
    """The built package and imported runtime must expose the same version."""
    assert version("omninet-v4") == __version__
