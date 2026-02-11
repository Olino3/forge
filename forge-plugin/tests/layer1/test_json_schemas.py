"""Test JSON schemas and validate all JSON config files.

Validates:
- All 11 agent *.config.json files against agent_config.schema.json
- hooks.json structure (valid event types)
- plugin.json required fields and command path resolution
- root_safety_profile.json structure
- framework_conflicts.json validity

Phase 1 of the Forge Testing Architecture.
"""

import json
import re
import sys
from pathlib import Path

import pytest

# Allow running standalone: python3 tests/layer1/test_json_schemas.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, load_json


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_EVENT_TYPES = {
    "PreToolUse",
    "PostToolUse",
    "SessionStart",
    "UserPromptSubmit",
    "Stop",
    "PreCompact",
    "TaskCompleted",
    "SubagentStart",
    "SessionEnd",
}

VALID_DOMAINS = {
    "engineering",
    "angular",
    "azure",
    "commands",
    "dotnet",
    "git",
    "python",
    "schema",
    "security",
}

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_schema(name: str) -> dict:
    """Load a JSON schema from the interfaces/schemas directory."""
    schema_path = FORGE_DIR / "interfaces" / "schemas" / name
    assert schema_path.exists(), f"Schema not found: {schema_path}"
    return load_json(schema_path)


def _get_agent_configs() -> list[tuple[str, Path]]:
    """Return list of (agent_name, config_path) tuples."""
    agents_dir = FORGE_DIR / "agents"
    configs = sorted(agents_dir.glob("*.config.json"))
    return [(p.name.replace(".config.json", ""), p) for p in configs]


# ---------------------------------------------------------------------------
# Agent Config Tests
# ---------------------------------------------------------------------------


class TestAgentConfigSchemas:
    """Validate all agent config.json files against the JSON schema."""

    @pytest.fixture(scope="class")
    def schema(self):
        return _load_schema("agent_config.schema.json")

    @pytest.fixture(scope="class")
    def agent_configs(self):
        return _get_agent_configs()

    def test_agent_configs_exist(self, agent_configs):
        """At least one agent config must exist."""
        assert len(agent_configs) > 0, "No agent config files found"

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_config_valid_json(self, agent_name, config_path):
        """Each agent config must be valid JSON."""
        try:
            load_json(config_path)
        except json.JSONDecodeError as e:
            pytest.fail(f"{config_path.name}: Invalid JSON — {e}")

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_config_schema_compliance(self, agent_name, config_path, schema):
        """Each agent config must validate against agent_config.schema.json."""
        from jsonschema import validate, ValidationError

        config = load_json(config_path)
        # Strip $schema meta-property — it's not a data field
        config_for_validation = {k: v for k, v in config.items() if k != "$schema"}
        try:
            validate(instance=config_for_validation, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{config_path.name}: Schema violation — {e.message}")

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_config_name_matches_filename(self, agent_name, config_path):
        """Agent config 'name' field must match the filename prefix."""
        config = load_json(config_path)
        assert config.get("name") == agent_name, (
            f"{config_path.name}: 'name' is '{config.get('name')}' "
            f"but filename implies '{agent_name}'"
        )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_config_version_semver(self, agent_name, config_path):
        """Agent config 'version' must match semver pattern."""
        config = load_json(config_path)
        version = config.get("version", "")
        assert SEMVER_PATTERN.match(version), (
            f"{config_path.name}: version '{version}' is not valid semver"
        )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_config_primary_domains_valid(self, agent_name, config_path):
        """Agent config primaryDomains must use valid domain enum values."""
        config = load_json(config_path)
        domains = config.get("context", {}).get("primaryDomains", [])
        for domain in domains:
            assert domain in VALID_DOMAINS, (
                f"{config_path.name}: primaryDomain '{domain}' not in valid domains"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_config_has_paired_markdown(self, agent_name, config_path):
        """Each agent config must have a paired .md file."""
        md_path = config_path.parent / f"{agent_name}.md"
        assert md_path.exists(), (
            f"{agent_name}: Missing paired markdown file {md_path.name}"
        )


# ---------------------------------------------------------------------------
# hooks.json Tests
# ---------------------------------------------------------------------------


class TestHooksJson:
    """Validate hooks.json structure and event types."""

    @pytest.fixture(scope="class")
    def hooks_data(self):
        hooks_path = FORGE_DIR / "hooks" / "hooks.json"
        assert hooks_path.exists(), "hooks.json not found"
        return load_json(hooks_path)

    def test_hooks_json_has_hooks_key(self, hooks_data):
        """hooks.json must have a top-level 'hooks' key."""
        assert "hooks" in hooks_data, "hooks.json missing 'hooks' key"

    def test_hooks_event_types_valid(self, hooks_data):
        """All event type keys in hooks.json must be valid."""
        events = hooks_data.get("hooks", {})
        for event_type in events:
            assert event_type in VALID_EVENT_TYPES, (
                f"hooks.json: Invalid event type '{event_type}'. "
                f"Valid types: {VALID_EVENT_TYPES}"
            )

    def test_hooks_entries_have_hooks_array(self, hooks_data):
        """Each event type entry must contain hook definitions with 'hooks' arrays."""
        events = hooks_data.get("hooks", {})
        for event_type, matchers in events.items():
            assert isinstance(matchers, list), (
                f"hooks.json: '{event_type}' value must be a list"
            )
            for i, matcher_block in enumerate(matchers):
                assert "hooks" in matcher_block, (
                    f"hooks.json: '{event_type}'[{i}] missing 'hooks' key"
                )
                assert isinstance(matcher_block["hooks"], list), (
                    f"hooks.json: '{event_type}'[{i}]['hooks'] must be a list"
                )

    def test_hooks_commands_are_strings(self, hooks_data):
        """Each hook command must be a non-empty string."""
        events = hooks_data.get("hooks", {})
        for event_type, matchers in events.items():
            for matcher_block in matchers:
                for hook in matcher_block.get("hooks", []):
                    assert "command" in hook, (
                        f"hooks.json: hook in '{event_type}' missing 'command'"
                    )
                    assert isinstance(hook["command"], str) and hook["command"].strip(), (
                        f"hooks.json: hook command in '{event_type}' is empty"
                    )

    def test_hooks_reference_existing_scripts(self, hooks_data):
        """Hook commands must reference scripts that exist on disk."""
        events = hooks_data.get("hooks", {})
        for event_type, matchers in events.items():
            for matcher_block in matchers:
                for hook in matcher_block.get("hooks", []):
                    cmd = hook.get("command", "")
                    # Extract script path from: bash "${CLAUDE_PLUGIN_ROOT}/hooks/script.sh"
                    match = re.search(r'hooks/([a-z_]+\.sh)', cmd)
                    if match:
                        script_name = match.group(1)
                        script_path = FORGE_DIR / "hooks" / script_name
                        assert script_path.exists(), (
                            f"hooks.json: '{event_type}' references "
                            f"non-existent script '{script_name}'"
                        )


# ---------------------------------------------------------------------------
# plugin.json Tests
# ---------------------------------------------------------------------------


class TestPluginJson:
    """Validate plugin.json structure and command paths."""

    @pytest.fixture(scope="class")
    def plugin_data(self):
        plugin_path = FORGE_DIR / ".claude-plugin" / "plugin.json"
        assert plugin_path.exists(), "plugin.json not found at .claude-plugin/plugin.json"
        return load_json(plugin_path)

    def test_plugin_has_name(self, plugin_data):
        """plugin.json must have a 'name' field."""
        assert "name" in plugin_data, "plugin.json missing 'name'"
        assert isinstance(plugin_data["name"], str) and plugin_data["name"].strip()

    def test_plugin_has_version(self, plugin_data):
        """plugin.json must have a valid semver 'version' field."""
        assert "version" in plugin_data, "plugin.json missing 'version'"
        assert SEMVER_PATTERN.match(plugin_data["version"]), (
            f"plugin.json version '{plugin_data['version']}' is not valid semver"
        )

    def test_plugin_has_commands(self, plugin_data):
        """plugin.json must have a 'commands' object."""
        assert "commands" in plugin_data, "plugin.json missing 'commands'"
        assert isinstance(plugin_data["commands"], dict)
        assert len(plugin_data["commands"]) > 0, "plugin.json 'commands' is empty"

    def test_plugin_command_paths_exist(self, plugin_data):
        """All command paths in plugin.json must resolve to existing files."""
        commands = plugin_data.get("commands", {})
        for cmd_name, cmd_path in commands.items():
            full_path = FORGE_DIR / cmd_path
            assert full_path.exists(), (
                f"plugin.json: command '{cmd_name}' points to "
                f"non-existent path '{cmd_path}'"
            )

    def test_plugin_lists_expected_command_count(self, plugin_data):
        """plugin.json should list all 12 commands."""
        commands = plugin_data.get("commands", {})
        assert len(commands) >= 12, (
            f"plugin.json has {len(commands)} commands, expected at least 12"
        )


# ---------------------------------------------------------------------------
# root_safety_profile.json Tests
# ---------------------------------------------------------------------------


class TestRootSafetyProfile:
    """Validate root_safety_profile.json structure."""

    @pytest.fixture(scope="class")
    def safety_data(self):
        safety_path = FORGE_DIR / "templates" / "root_safety_profile.json"
        assert safety_path.exists(), "root_safety_profile.json not found"
        return load_json(safety_path)

    def test_safety_has_version(self, safety_data):
        """Safety profile must have a version."""
        assert "version" in safety_data
        assert SEMVER_PATTERN.match(safety_data["version"])

    def test_safety_has_allowed_tools(self, safety_data):
        """Safety profile must define allowed tools."""
        assert "allowedTools" in safety_data
        assert isinstance(safety_data["allowedTools"], list)
        assert len(safety_data["allowedTools"]) > 0

    def test_safety_has_context_limits(self, safety_data):
        """Safety profile must define context limits."""
        assert "contextLimits" in safety_data
        limits = safety_data["contextLimits"]
        expected_keys = [
            "maxMemoryFileSizeLines",
            "maxProjectOverviewLines",
            "maxReviewHistoryLines",
            "stalenessThresholdDays",
            "agingThresholdDays",
        ]
        for key in expected_keys:
            assert key in limits, f"contextLimits missing '{key}'"
            assert isinstance(limits[key], int), f"contextLimits.{key} must be int"
            assert limits[key] > 0, f"contextLimits.{key} must be positive"

    def test_safety_has_required_structure(self, safety_data):
        """Safety profile must define required directories and files."""
        assert "requiredStructure" in safety_data
        rs = safety_data["requiredStructure"]
        assert "directories" in rs
        assert "files" in rs
        assert isinstance(rs["directories"], list)
        assert isinstance(rs["files"], list)

    def test_safety_has_sandbox_boundary(self, safety_data):
        """Safety profile must define sandbox boundary rules."""
        assert "sandboxBoundary" in safety_data
        sb = safety_data["sandboxBoundary"]
        assert "allowedPathPrefixes" in sb
        assert "deniedPathPatterns" in sb
        assert "deniedFilePatterns" in sb


# ---------------------------------------------------------------------------
# framework_conflicts.json Tests
# ---------------------------------------------------------------------------


class TestFrameworkConflicts:
    """Validate framework_conflicts.json structure."""

    @pytest.fixture(scope="class")
    def conflicts_data(self):
        conflicts_path = FORGE_DIR / "hooks" / "lib" / "framework_conflicts.json"
        assert conflicts_path.exists(), "framework_conflicts.json not found"
        return load_json(conflicts_path)

    def test_conflicts_is_valid_json(self, conflicts_data):
        """framework_conflicts.json must be valid JSON (loaded successfully)."""
        assert isinstance(conflicts_data, dict)

    def test_conflicts_has_entries(self, conflicts_data):
        """framework_conflicts.json must have at least one conflict group."""
        assert len(conflicts_data) > 0, "framework_conflicts.json is empty"

    def test_conflicts_groups_are_valid(self, conflicts_data):
        """Each conflict group must have description + members with >=2 frameworks."""
        for group_name, group in conflicts_data.items():
            # Skip meta-keys like _comment
            if group_name.startswith("_"):
                continue
            assert isinstance(group, dict), (
                f"Conflict group '{group_name}' must be dict"
            )
            assert "description" in group, (
                f"Conflict group '{group_name}' missing 'description'"
            )
            assert "members" in group, (
                f"Conflict group '{group_name}' missing 'members'"
            )
            members = group["members"]
            assert isinstance(members, dict), (
                f"Conflict group '{group_name}' members must be dict"
            )
            assert len(members) >= 2, (
                f"Conflict group '{group_name}' needs at least 2 members"
            )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
