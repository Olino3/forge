"""Test hook registration completeness.

Validates:
- Every active .sh file in hooks/ is registered in hooks.json
- Every script path in hooks.json exists on disk
- Known legacy/inactive scripts are accounted for
- No duplicate hook registrations (same script + same event)

Phase 2 of the Forge Testing Architecture.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, load_json


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOOKS_DIR = FORGE_DIR / "hooks"

# Scripts that exist as files but are intentionally NOT registered in hooks.json.
# These are legacy, deprecated, or sourced-only scripts.
KNOWN_UNREGISTERED_SCRIPTS = {
    "memory_sync.sh",
    "context_freshness.sh",
}

VALID_EVENT_TYPES = {
    "PreToolUse", "PostToolUse", "SessionStart", "UserPromptSubmit",
    "Stop", "PreCompact", "TaskCompleted", "SubagentStart", "SessionEnd",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_hook_scripts_on_disk() -> set[str]:
    """Return set of .sh filenames directly in hooks/ (not lib/)."""
    return {
        f.name
        for f in HOOKS_DIR.iterdir()
        if f.is_file() and f.suffix == ".sh"
    }


def _get_registered_scripts(hooks_data: dict) -> set[str]:
    """Extract all script names referenced in hooks.json."""
    scripts = set()
    events = hooks_data.get("hooks", {})
    for matchers in events.values():
        for matcher_block in matchers:
            for hook in matcher_block.get("hooks", []):
                cmd = hook.get("command", "")
                match = re.search(r'hooks/([a-z_]+\.sh)', cmd)
                if match:
                    scripts.add(match.group(1))
    return scripts


def _get_registrations(hooks_data: dict) -> list[tuple[str, str]]:
    """Return list of (event_type, script_name) tuples for all registrations."""
    registrations = []
    events = hooks_data.get("hooks", {})
    for event_type, matchers in events.items():
        for matcher_block in matchers:
            for hook in matcher_block.get("hooks", []):
                cmd = hook.get("command", "")
                match = re.search(r'hooks/([a-z_]+\.sh)', cmd)
                if match:
                    registrations.append((event_type, match.group(1)))
    return registrations


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestHookRegistration:
    """Validate hook registration completeness."""

    @pytest.fixture(scope="class")
    def hooks_data(self):
        hooks_path = HOOKS_DIR / "hooks.json"
        assert hooks_path.exists(), "hooks.json not found"
        return load_json(hooks_path)

    def test_hooks_json_exists(self):
        """hooks.json must exist."""
        assert (HOOKS_DIR / "hooks.json").exists()

    def test_active_scripts_are_registered(self, hooks_data):
        """Every active .sh file (not in KNOWN_UNREGISTERED) must be in hooks.json."""
        on_disk = _get_hook_scripts_on_disk()
        registered = _get_registered_scripts(hooks_data)
        active_on_disk = on_disk - KNOWN_UNREGISTERED_SCRIPTS

        unregistered = active_on_disk - registered
        assert not unregistered, (
            f"Hook scripts exist on disk but are not registered in hooks.json: "
            f"{sorted(unregistered)}. If intentionally unregistered, add them to "
            f"KNOWN_UNREGISTERED_SCRIPTS in test_hooks_registration.py"
        )

    def test_registered_scripts_exist_on_disk(self, hooks_data):
        """Every script in hooks.json must exist as a file in hooks/."""
        on_disk = _get_hook_scripts_on_disk()
        registered = _get_registered_scripts(hooks_data)

        missing = registered - on_disk
        assert not missing, (
            f"hooks.json references scripts that don't exist on disk: "
            f"{sorted(missing)}"
        )

    def test_known_unregistered_exist(self):
        """Known unregistered scripts must still exist on disk."""
        on_disk = _get_hook_scripts_on_disk()
        for script in KNOWN_UNREGISTERED_SCRIPTS:
            assert script in on_disk, (
                f"Known unregistered script '{script}' no longer exists. "
                f"Remove it from KNOWN_UNREGISTERED_SCRIPTS."
            )

    def test_event_types_are_valid(self, hooks_data):
        """All event type keys must be valid Claude Code events."""
        events = hooks_data.get("hooks", {})
        for event_type in events:
            assert event_type in VALID_EVENT_TYPES, (
                f"hooks.json: Invalid event type '{event_type}'"
            )

    def test_no_duplicate_registrations(self, hooks_data):
        """No script should be registered twice for the same event+matcher combo."""
        events = hooks_data.get("hooks", {})
        for event_type, matchers in events.items():
            for i, matcher_block in enumerate(matchers):
                matcher = matcher_block.get("matcher", "")
                scripts_in_block = []
                for hook in matcher_block.get("hooks", []):
                    cmd = hook.get("command", "")
                    match = re.search(r'hooks/([a-z_]+\.sh)', cmd)
                    if match:
                        script_name = match.group(1)
                        assert script_name not in scripts_in_block, (
                            f"hooks.json: '{script_name}' registered twice "
                            f"in {event_type}[matcher='{matcher}']"
                        )
                        scripts_in_block.append(script_name)

    def test_hook_count_is_expected(self, hooks_data):
        """hooks.json should register at least 20 unique hook scripts."""
        registered = _get_registered_scripts(hooks_data)
        assert len(registered) >= 20, (
            f"Expected at least 20 registered hook scripts, found {len(registered)}: "
            f"{sorted(registered)}"
        )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
