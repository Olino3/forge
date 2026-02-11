"""Shared pytest configuration and helpers for Forge test suite.

Provides:
- FORGE_DIR resolution (absolute path to forge-plugin/)
- YAML frontmatter extraction helper
- Common path constants
"""

import os
import re
import sys
from pathlib import Path

import pytest


def _resolve_forge_dir() -> Path:
    """Resolve the absolute path to the forge-plugin directory.

    Search order:
    1. FORGE_DIR environment variable
    2. Walk up from this file to find forge-plugin/
    """
    env_dir = os.environ.get("FORGE_DIR")
    if env_dir:
        p = Path(env_dir).resolve()
        if p.is_dir():
            return p

    # Walk up from tests/ directory to find forge-plugin/
    current = Path(__file__).resolve().parent
    while current != current.parent:
        candidate = current / "forge-plugin"
        if candidate.is_dir():
            return candidate
        # Also check if we're inside forge-plugin already
        if current.name == "forge-plugin":
            return current
        current = current.parent

    # Fallback: assume tests/ is inside forge-plugin/
    return Path(__file__).resolve().parent.parent


FORGE_DIR = _resolve_forge_dir()
"""Absolute path to the forge-plugin/ directory."""

REPO_ROOT = FORGE_DIR.parent
"""Absolute path to the repository root."""


def extract_yaml_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file.

    Expects frontmatter delimited by --- at the top of the file.
    Returns parsed dict or None if no frontmatter found.
    """
    import yaml

    text = filepath.read_text(encoding="utf-8")

    # Must start with ---
    if not text.startswith("---"):
        return None

    # Find closing ---
    end = text.find("---", 3)
    if end == -1:
        return None

    frontmatter_text = text[3:end].strip()
    if not frontmatter_text:
        return None

    try:
        return yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None


def load_json(filepath: Path) -> dict:
    """Load and parse a JSON file."""
    import json

    return json.loads(filepath.read_text(encoding="utf-8"))


# Pytest fixtures available to all tests


@pytest.fixture(scope="session")
def forge_dir() -> Path:
    """Provide the forge-plugin directory path."""
    return FORGE_DIR


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Provide the repository root path."""
    return REPO_ROOT
