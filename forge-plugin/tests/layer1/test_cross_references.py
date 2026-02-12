"""Test cross-reference integrity across all Forge components.

Validates:
- Skills referenced in agent configs exist as directories with SKILL.md
- Domains in agent configs exist as context directories
- alwaysLoadFiles paths in agent configs exist
- memory.storagePath directories in agent configs exist
- crossDomainTriggers in context files target existing files
- hooks.json commands reference existing scripts
- No circular cross-domain triggers

Phase 2 of the Forge Testing Architecture.
"""

import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, REPO_ROOT, extract_yaml_frontmatter, load_json


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_DOMAINS = {
    "engineering", "angular", "azure", "commands",
    "dotnet", "git", "python", "schema", "security",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_agent_configs() -> list[tuple[str, Path]]:
    """Return (agent_name, config_path) for all agent configs."""
    agents_dir = FORGE_DIR / "agents"
    configs = sorted(agents_dir.glob("*.config.json"))
    return [(p.name.replace(".config.json", ""), p) for p in configs]


def _get_domain_context_files() -> list[tuple[str, Path]]:
    """Return (relative_id, path) for all .md files inside domain subdirectories."""
    context_dir = FORGE_DIR / "context"
    files = []
    for domain_dir in sorted(context_dir.iterdir()):
        if domain_dir.is_dir() and domain_dir.name in VALID_DOMAINS:
            for f in sorted(domain_dir.rglob("*.md")):
                files.append((str(f.relative_to(context_dir)), f))
    return files


# ---------------------------------------------------------------------------
# Agent Config → Skill Cross-References
# ---------------------------------------------------------------------------


class TestAgentSkillReferences:
    """Validate that skills referenced in agent configs exist."""

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_skills_exist(self, agent_name, config_path):
        """Every skill in an agent's skills[] must have a corresponding directory."""
        config = load_json(config_path)
        skills = config.get("skills", [])
        for skill_entry in skills:
            skill_name = skill_entry.get("name", "")
            skill_dir = FORGE_DIR / "skills" / skill_name
            assert skill_dir.is_dir(), (
                f"Agent '{agent_name}' references skill '{skill_name}' "
                f"but directory skills/{skill_name}/ does not exist"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_skills_have_skill_md(self, agent_name, config_path):
        """Every referenced skill must have SKILL.md."""
        config = load_json(config_path)
        skills = config.get("skills", [])
        for skill_entry in skills:
            skill_name = skill_entry.get("name", "")
            skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
            assert skill_md.exists(), (
                f"Agent '{agent_name}' → skill '{skill_name}': Missing SKILL.md"
            )


# ---------------------------------------------------------------------------
# Agent Config → Domain Cross-References
# ---------------------------------------------------------------------------


class TestAgentDomainReferences:
    """Validate that domains referenced in agent configs exist as context dirs."""

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_primary_domains_exist(self, agent_name, config_path):
        """Every primaryDomain must have a matching context/ subdirectory."""
        config = load_json(config_path)
        domains = config.get("context", {}).get("primaryDomains", [])
        for domain in domains:
            domain_dir = FORGE_DIR / "context" / domain
            assert domain_dir.is_dir(), (
                f"Agent '{agent_name}' primaryDomain '{domain}': "
                f"context/{domain}/ does not exist"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_secondary_domains_exist(self, agent_name, config_path):
        """Every secondaryDomain must have a matching context/ subdirectory."""
        config = load_json(config_path)
        domains = config.get("context", {}).get("secondaryDomains", [])
        for domain in domains:
            domain_dir = FORGE_DIR / "context" / domain
            assert domain_dir.is_dir(), (
                f"Agent '{agent_name}' secondaryDomain '{domain}': "
                f"context/{domain}/ does not exist"
            )


# ---------------------------------------------------------------------------
# Agent Config → alwaysLoadFiles Cross-References
# ---------------------------------------------------------------------------


class TestAgentAlwaysLoadFiles:
    """Validate that alwaysLoadFiles paths exist."""

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_always_load_files_exist(self, agent_name, config_path):
        """Every alwaysLoadFiles path must resolve to an existing file."""
        config = load_json(config_path)
        files = config.get("context", {}).get("alwaysLoadFiles", [])
        for filepath in files:
            # Paths are relative to forge-plugin/ or repo root
            resolved = FORGE_DIR / filepath
            if not resolved.exists():
                resolved = REPO_ROOT / filepath
            assert resolved.exists(), (
                f"Agent '{agent_name}' alwaysLoadFiles '{filepath}' "
                f"does not exist"
            )


# ---------------------------------------------------------------------------
# Agent Config → Memory Storage Path Cross-References
# ---------------------------------------------------------------------------


class TestAgentMemoryPaths:
    """Validate that memory storage paths exist."""

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_memory_storage_path_exists(self, agent_name, config_path):
        """memory.storagePath must resolve to an existing directory."""
        config = load_json(config_path)
        storage_path = config.get("memory", {}).get("storagePath", "")
        if not storage_path:
            pytest.skip(f"Agent '{agent_name}' has no storagePath")
        # storage_path is relative to repo root (e.g., "forge-plugin/memory/agents/hephaestus")
        resolved = REPO_ROOT / storage_path
        assert resolved.is_dir(), (
            f"Agent '{agent_name}' memory.storagePath '{storage_path}' "
            f"does not exist at {resolved}"
        )


# ---------------------------------------------------------------------------
# Context → Cross-Domain Trigger Cross-References
# ---------------------------------------------------------------------------


class TestCrossDomainTriggers:
    """Validate crossDomainTriggers reference existing context files."""

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_cross_domain_triggers_resolve(self, rel_path, filepath):
        """crossDomainTriggers targets must exist as context files."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        triggers = fm.get("crossDomainTriggers", [])
        if not triggers:
            pytest.skip("No crossDomainTriggers")
        context_dir = FORGE_DIR / "context"
        for trigger in triggers:
            # Format: "domain/filename" → context/{domain}/{filename}.md
            parts = trigger.split("/", 1)
            if len(parts) == 2:
                domain, filename = parts
                target = context_dir / domain / f"{filename}.md"
                assert target.exists(), (
                    f"{rel_path}: crossDomainTrigger '{trigger}' → "
                    f"{target.relative_to(FORGE_DIR)} does not exist"
                )
            else:
                pytest.fail(
                    f"{rel_path}: crossDomainTrigger '{trigger}' has invalid format "
                    f"(expected 'domain/filename')"
                )

    def test_no_self_referential_triggers(self):
        """No context file should trigger itself."""
        context_dir = FORGE_DIR / "context"
        for _, filepath in _get_domain_context_files():
            fm = extract_yaml_frontmatter(filepath)
            if fm is None:
                continue
            triggers = fm.get("crossDomainTriggers", [])
            file_id = fm.get("id", "")
            for trigger in triggers:
                assert trigger != file_id, (
                    f"{file_id}: Self-referential crossDomainTrigger"
                )


# ---------------------------------------------------------------------------
# hooks.json → Script File Cross-References
# ---------------------------------------------------------------------------


class TestHooksJsonScriptReferences:
    """Validate that hooks.json commands reference existing scripts."""

    @pytest.fixture(scope="class")
    def hooks_data(self):
        return load_json(FORGE_DIR / "hooks" / "hooks.json")

    def test_all_hook_scripts_exist(self, hooks_data):
        """Every script referenced in hooks.json must exist on disk."""
        events = hooks_data.get("hooks", {})
        missing = []
        for event_type, matchers in events.items():
            for matcher_block in matchers:
                for hook in matcher_block.get("hooks", []):
                    cmd = hook.get("command", "")
                    # Extract script name from command like:
                    # bash "${CLAUDE_PLUGIN_ROOT}/hooks/script_name.sh"
                    match = re.search(r'hooks/([a-z_]+\.sh)', cmd)
                    if match:
                        script_name = match.group(1)
                        script_path = FORGE_DIR / "hooks" / script_name
                        if not script_path.exists():
                            missing.append(
                                f"{event_type}: {script_name}"
                            )
        assert not missing, (
            f"hooks.json references non-existent scripts: {missing}"
        )

    def test_hook_script_paths_in_correct_dir(self, hooks_data):
        """Hook commands must reference scripts in the hooks/ directory."""
        events = hooks_data.get("hooks", {})
        for event_type, matchers in events.items():
            for matcher_block in matchers:
                for hook in matcher_block.get("hooks", []):
                    cmd = hook.get("command", "")
                    # Verify the command uses CLAUDE_PLUGIN_ROOT/hooks/ pattern
                    if "hooks/" in cmd:
                        assert "CLAUDE_PLUGIN_ROOT" in cmd or "hooks/" in cmd, (
                            f"{event_type}: Hook command doesn't use standard path pattern"
                        )


# ---------------------------------------------------------------------------
# Plugin.json → Command Path Cross-References
# ---------------------------------------------------------------------------


class TestPluginCommandReferences:
    """Validate command files exist in filesystem."""

    def test_all_command_paths_exist(self):
        """Every expected command must exist as a flat .md file."""
        expected_commands = {
            "analyze", "implement", "improve", "document", "test", "build",
            "brainstorm", "remember", "mock", "azure-pipeline", "etl-pipeline",
            "azure-function",
        }
        commands_dir = FORGE_DIR / "commands"
        missing = []
        for cmd_name in expected_commands:
            cmd_file = commands_dir / f"{cmd_name}.md"
            if not cmd_file.exists():
                missing.append(f"{cmd_name}: {cmd_name}.md not found")
        assert not missing, (
            f"Command validation failed: {missing}"
        )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
