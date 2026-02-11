"""Layer 2 Memory Testing — Pytest fixtures.

Provides the temp_forge_env factory fixture for memory lifecycle tests.
"""

import pytest

from layer2.hooks.hook_helpers import TempForgeEnvironment


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
