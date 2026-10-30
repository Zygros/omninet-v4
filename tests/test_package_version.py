"""Regression checks for the OmniNet package version metadata."""

from pathlib import Path
import re

from omninet import __version__


def test_project_and_runtime_versions_match_and_use_pep440_local_label():
    """Keep Poetry, legacy setuptools, and runtime version declarations aligned."""
    root = Path(__file__).resolve().parents[1]
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    setup = (root / "setup.py").read_text(encoding="utf-8")

    project_version = re.search(r'(?m)^version\s*=\s*"([^"]+)"$', pyproject)
    setup_version = re.search(r'(?m)^\s*version\s*=\s*"([^"]+)"', setup)

    assert project_version is not None
    assert setup_version is not None
    assert project_version.group(1) == setup_version.group(1) == __version__
    assert re.fullmatch(r"\d+\.\d+\.\d+\+[a-z0-9]+", __version__)
