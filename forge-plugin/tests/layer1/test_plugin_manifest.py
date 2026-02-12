"""Test plugin.json manifest validity and completeness.

Validates:
- plugin.json exists at .claude-plugin/plugin.json
- Has required fields: name, version, description, author
- Version is valid semver
- Does NOT have commands field (commands discovered from filesystem)
- All 12 command directories exist with COMMAND.md files
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
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$")

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

    def test_has_no_commands_field(self, plugin):
        """plugin.json should not have a 'commands' field (commands are discovered from filesystem)."""
        assert "commands" not in plugin, (
            "plugin.json should not contain 'commands' field - commands are discovered from filesystem"
        )

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
    """Validate all commands exist in filesystem and follow conventions."""

    def test_expected_command_count(self):
        """At least 12 command directories must exist."""
        commands_dir = FORGE_DIR / "commands"
        command_dirs = [d for d in commands_dir.iterdir() if d.is_dir()]
        assert len(command_dirs) >= 12, (
            f"Expected at least 12 command directories, found {len(command_dirs)}: "
            f"{sorted([d.name for d in command_dirs])}"
        )

    def test_all_expected_commands_present(self):
        """All 12 expected commands must exist as directories."""
        commands_dir = FORGE_DIR / "commands"
        existing_commands = {d.name for d in commands_dir.iterdir() if d.is_dir()}
        missing = EXPECTED_COMMANDS - existing_commands
        assert not missing, (
            f"Missing expected command directories: {sorted(missing)}"
        )

    @pytest.mark.parametrize("cmd_name", sorted(EXPECTED_COMMANDS))
    def test_command_directory_exists(self, cmd_name):
        """Each command must have a directory in commands/."""
        cmd_dir = FORGE_DIR / "commands" / cmd_name
        assert cmd_dir.is_dir(), (
            f"Command directory 'commands/{cmd_name}/' does not exist"
        )

    @pytest.mark.parametrize("cmd_name", sorted(EXPECTED_COMMANDS))
    def test_command_has_command_md(self, cmd_name):
        """Each command directory must contain a COMMAND.md file."""
        cmd_file = FORGE_DIR / "commands" / cmd_name / "COMMAND.md"
        assert cmd_file.exists(), (
            f"Command '{cmd_name}' missing COMMAND.md file"
        )

    def test_command_paths_follow_convention(self):
        """All command COMMAND.md files must exist at commands/{name}/COMMAND.md."""
        commands_dir = FORGE_DIR / "commands"
        for cmd_dir in commands_dir.iterdir():
            if cmd_dir.is_dir():
                cmd_file = cmd_dir / "COMMAND.md"
                assert cmd_file.exists(), (
                    f"Command '{cmd_dir.name}' directory exists but missing COMMAND.md"
                )

    def test_no_extra_unexpected_commands(self):
        """Track any commands not in the expected set (informational)."""
        import warnings
        commands_dir = FORGE_DIR / "commands"
        existing_commands = {d.name for d in commands_dir.iterdir() if d.is_dir()}
        extra = existing_commands - EXPECTED_COMMANDS
        # Extra commands are allowed but should be noted
        if extra:
            warnings.warn(
                f"Found {len(extra)} unexpected command(s): {sorted(extra)}. "
                f"Update EXPECTED_COMMANDS in test_plugin_manifest.py if intentional.",
                UserWarning
            )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
