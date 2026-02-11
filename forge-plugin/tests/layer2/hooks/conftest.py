"""Layer 2 Hook Testing Infrastructure — Pytest fixtures.

Classes and constants are in hook_helpers.py to avoid import conflicts
with the root-level tests/conftest.py.
"""

from pathlib import Path

import pytest

from layer2.hooks.hook_helpers import (
    HookRunner,
    TempForgeEnvironment,
    FORGE_DIR,
    REPO_ROOT,
)


# ── Pytest Fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def hook_runner():
    """Factory fixture that creates a HookRunner for a given script name."""
    def _make(script_name: str, timeout: int = 10) -> HookRunner:
        return HookRunner(script_name, timeout=timeout)
    return _make


@pytest.fixture
def temp_forge_env():
    """Factory fixture that creates a TempForgeEnvironment."""
    envs = []

    def _make(init_git: bool = False) -> TempForgeEnvironment:
        env = TempForgeEnvironment(init_git=init_git)
        env.__enter__()
        envs.append(env)
        return env

    yield _make

    for env in envs:
        env.__exit__(None, None, None)


@pytest.fixture(scope="session")
def forge_dir() -> Path:
    """Provide the forge-plugin directory path."""
    return FORGE_DIR


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Provide the repository root path."""
    return REPO_ROOT
