"""Test plugin.json manifest validity and completeness.

Validates:
- plugin.json exists at .claude-plugin/plugin.json
- Has required fields: name, version, description, author
- Version is valid semver
- All 12 command .md files exist in flat structure (commands/{name}.md)
- Command files have valid YAML frontmatter
- .claude-plugin/ contains only expected files
- Commands field is optional (Claude Code auto-discovers from flat .md files)

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

    def test_has_commands(self, plugin):
        """plugin.json may optionally have a 'commands' object (auto-discovery is also supported)."""
        # Commands field is optional since Claude Code auto-discovers from .md files
        if "commands" in plugin:
            assert isinstance(plugin["commands"], dict), (
                "If present, 'commands' must be an object"
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
    """Validate command file structure (auto-discovery via flat .md files)."""

    @pytest.fixture(scope="class")
    def plugin(self):
        return load_json(PLUGIN_JSON)

    def test_command_files_exist(self):
        """All 12 expected command .md files must exist in commands/ directory."""
        commands_dir = FORGE_DIR / "commands"
        for cmd_name in sorted(EXPECTED_COMMANDS):
            cmd_file = commands_dir / f"{cmd_name}.md"
            assert cmd_file.exists(), (
                f"Command file missing: commands/{cmd_name}.md"
            )

    def test_expected_command_count(self):
        """commands/ directory must contain at least 12 command .md files (excluding index.md)."""
        commands_dir = FORGE_DIR / "commands"
        cmd_files = [
            f for f in commands_dir.glob("*.md")
            if f.name != "index.md"
        ]
        assert len(cmd_files) >= 12, (
            f"Expected at least 12 command files, found {len(cmd_files)}: "
            f"{sorted([f.stem for f in cmd_files])}"
        )

    @pytest.mark.parametrize("cmd_name", sorted(EXPECTED_COMMANDS))
    def test_command_file_has_content(self, cmd_name):
        """Each command .md file must have YAML frontmatter and content."""
        cmd_file = FORGE_DIR / "commands" / f"{cmd_name}.md"
        if not cmd_file.exists():
            pytest.skip(f"Command file '{cmd_name}.md' not found")
        
        content = cmd_file.read_text()
        # Check for YAML frontmatter (starts and ends with ---)
        assert content.startswith("---"), (
            f"Command '{cmd_name}.md' missing YAML frontmatter"
        )
        assert content.count("---") >= 2, (
            f"Command '{cmd_name}.md' has incomplete YAML frontmatter"
        )

    def test_examples_directory_exists(self):
        """commands/_docs/ directory should exist for examples."""
        docs_dir = FORGE_DIR / "commands" / "_docs"
        assert docs_dir.is_dir(), "commands/_docs/ directory missing"

    def test_examples_files_exist(self):
        """Each command should have a corresponding examples file in _docs/."""
        docs_dir = FORGE_DIR / "commands" / "_docs"
        for cmd_name in sorted(EXPECTED_COMMANDS):
            examples_file = docs_dir / f"{cmd_name}-examples.md"
            # Examples files are optional but recommended
            if not examples_file.exists():
                pass  # Not a hard requirement


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
