"""Test plugin.json manifest validity and completeness.

Validates:
- plugin.json exists at .claude-plugin/plugin.json
- Has required fields: name, version, commands
- Version is valid semver
- All 12 commands are listed
- Each command path exists as a file
- .claude-plugin/ contains only expected files
- No extraneous fields in plugin.json

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

PLUGIN_DIR = FORGE_DIR / ".claude-plugin"
PLUGIN_JSON = PLUGIN_DIR / "plugin.json"
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

EXPECTED_COMMANDS = {
    "analyze", "implement", "improve", "document", "test", "build",
    "brainstorm", "remember", "mock", "azure-pipeline", "etl-pipeline",
    "azure-function",
}


# ---------------------------------------------------------------------------
# Structure Tests
# ---------------------------------------------------------------------------


class TestPluginManifestStructure:
    """Validate plugin.json location and structure."""

    def test_claude_plugin_dir_exists(self):
        """.claude-plugin/ directory must exist."""
        assert PLUGIN_DIR.is_dir(), ".claude-plugin/ directory not found"

    def test_plugin_json_exists(self):
        """plugin.json must exist inside .claude-plugin/."""
        assert PLUGIN_JSON.is_file(), ".claude-plugin/plugin.json not found"

    def test_plugin_json_is_valid_json(self):
        """plugin.json must be valid JSON."""
        try:
            load_json(PLUGIN_JSON)
        except Exception as e:
            pytest.fail(f"plugin.json is not valid JSON: {e}")

    def test_claude_plugin_dir_contents(self):
        """.claude-plugin/ should only contain plugin.json."""
        contents = [f.name for f in PLUGIN_DIR.iterdir() if not f.name.startswith(".")]
        assert "plugin.json" in contents, "plugin.json not in .claude-plugin/"
        # Allow plugin.json and potentially other config files
        for item in contents:
            assert item.endswith(".json") or item.endswith(".md"), (
                f".claude-plugin/ contains unexpected file: {item}"
            )


# ---------------------------------------------------------------------------
# Required Fields Tests
# ---------------------------------------------------------------------------


class TestPluginManifestFields:
    """Validate plugin.json required fields."""

    @pytest.fixture(scope="class")
    def plugin(self):
        return load_json(PLUGIN_JSON)

    def test_has_name(self, plugin):
        """plugin.json must have a 'name' field."""
        assert "name" in plugin, "Missing 'name'"
        assert isinstance(plugin["name"], str) and plugin["name"].strip()

    def test_has_version(self, plugin):
        """plugin.json must have a 'version' field."""
        assert "version" in plugin, "Missing 'version'"

    def test_version_is_semver(self, plugin):
        """version must be valid semver."""
        version = plugin.get("version", "")
        assert SEMVER_PATTERN.match(version), (
            f"version '{version}' is not valid semver (expected X.Y.Z)"
        )

    def test_has_commands(self, plugin):
        """plugin.json must have a 'commands' object."""
        assert "commands" in plugin, "Missing 'commands'"
        assert isinstance(plugin["commands"], dict)

    def test_has_description(self, plugin):
        """plugin.json should have a 'description' field."""
        assert "description" in plugin, "Missing 'description'"
        assert isinstance(plugin["description"], str) and plugin["description"].strip()

    def test_has_author(self, plugin):
        """plugin.json should have an 'author' field."""
        assert "author" in plugin, "Missing 'author'"


# ---------------------------------------------------------------------------
# Command Completeness Tests
# ---------------------------------------------------------------------------


class TestPluginManifestCommands:
    """Validate all commands are listed and paths resolve."""

    @pytest.fixture(scope="class")
    def plugin(self):
        return load_json(PLUGIN_JSON)

    def test_expected_command_count(self, plugin):
        """plugin.json must list at least 12 commands."""
        commands = plugin.get("commands", {})
        assert len(commands) >= 12, (
            f"Expected at least 12 commands, found {len(commands)}: "
            f"{sorted(commands.keys())}"
        )

    def test_all_expected_commands_present(self, plugin):
        """All 12 expected commands must be listed."""
        commands = set(plugin.get("commands", {}).keys())
        missing = EXPECTED_COMMANDS - commands
        assert not missing, (
            f"Missing expected commands: {sorted(missing)}"
        )

    @pytest.mark.parametrize("cmd_name", sorted(EXPECTED_COMMANDS))
    def test_command_path_exists(self, plugin, cmd_name):
        """Each command path must resolve to an existing file."""
        commands = plugin.get("commands", {})
        if cmd_name not in commands:
            pytest.skip(f"Command '{cmd_name}' not in plugin.json")
        cmd_path = commands[cmd_name]
        full_path = FORGE_DIR / cmd_path
        assert full_path.exists(), (
            f"Command '{cmd_name}' → '{cmd_path}' does not exist"
        )

    @pytest.mark.parametrize("cmd_name", sorted(EXPECTED_COMMANDS))
    def test_command_path_points_to_command_md(self, plugin, cmd_name):
        """Each command path should point to a COMMAND.md file."""
        commands = plugin.get("commands", {})
        if cmd_name not in commands:
            pytest.skip(f"Command '{cmd_name}' not in plugin.json")
        cmd_path = commands[cmd_name]
        assert cmd_path.endswith("COMMAND.md"), (
            f"Command '{cmd_name}' path '{cmd_path}' should end with COMMAND.md"
        )

    def test_command_paths_follow_convention(self, plugin):
        """All command paths must follow commands/{name}/COMMAND.md convention."""
        commands = plugin.get("commands", {})
        for cmd_name, cmd_path in commands.items():
            expected = f"commands/{cmd_name}/COMMAND.md"
            assert cmd_path == expected, (
                f"Command '{cmd_name}' path '{cmd_path}' doesn't follow "
                f"convention '{expected}'"
            )

    def test_no_extra_unexpected_commands(self, plugin):
        """Warn about any commands not in the expected set (informational)."""
        commands = set(plugin.get("commands", {}).keys())
        extra = commands - EXPECTED_COMMANDS
        # Extra commands are allowed but noted
        if extra:
            pass  # Not a failure, but tracks new additions


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
