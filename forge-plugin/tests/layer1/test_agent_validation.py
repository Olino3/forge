"""Test agent configuration validation from forge-agent-validator workflow.

Validates:
1. Schema compliance against agent_config.schema.json
2. Skill references exist in forge-plugin/skills/
3. Context domain references exist under forge-plugin/context/
4. Memory directory exists
5. Personality file parity (.md + .config.json)
6. MCP references exist in forge-plugin/mcps/
7. Naming conventions (kebab-case, file matching)

Migrated from .github/workflows/forge-agent-validator.md as part of Phase 2 optimization.
"""

import json
import re
import sys
from pathlib import Path

import pytest
from jsonschema import validate, ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, load_json


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_DOMAINS = {
    "engineering", "angular", "azure", "commands",
    "dotnet", "git", "python", "schema", "security",
}

AGENT_SCHEMA_PATH = FORGE_DIR / "interfaces" / "schemas" / "agent_config.schema.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_agent_configs() -> list[tuple[str, Path]]:
    """Return (agent_name, config_path) for all agent configs."""
    agents_dir = FORGE_DIR / "agents"
    configs = sorted(agents_dir.glob("*.config.json"))
    # Extract agent name by removing .config.json suffix
    return [(p.name.replace(".config.json", ""), p) for p in configs]


def _is_kebab_case(name: str) -> bool:
    """Check if name follows kebab-case convention."""
    return bool(re.match(r'^[a-z]+(-[a-z]+)*$', name))


# ---------------------------------------------------------------------------
# Test Class
# ---------------------------------------------------------------------------

class TestAgentValidation:
    """Validate agent configurations per forge-agent-validator.md checks."""

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_schema_compliance(self, agent_name, config_path):
        """Check 1: Schema compliance against agent_config.schema.json."""
        config = load_json(config_path)
        schema = load_json(AGENT_SCHEMA_PATH)
        
        # Strip $schema meta-property — it's not a data field
        config_for_validation = {k: v for k, v in config.items() if k != "$schema"}
        
        try:
            validate(instance=config_for_validation, schema=schema)
        except ValidationError as e:
            pytest.fail(
                f"Agent '{agent_name}' config violates schema:\n"
                f"  Path: {' -> '.join(str(p) for p in e.path)}\n"
                f"  Error: {e.message}"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_skill_references_exist(self, agent_name, config_path):
        """Check 2: Every skill in config exists in forge-plugin/skills/."""
        config = load_json(config_path)
        skills = config.get("skills", [])
        
        for skill_entry in skills:
            skill_name = skill_entry.get("name", "")
            skill_dir = FORGE_DIR / "skills" / skill_name
            skill_md = skill_dir / "SKILL.md"
            
            assert skill_dir.is_dir(), (
                f"Agent '{agent_name}' references skill '{skill_name}' "
                f"but directory skills/{skill_name}/ does not exist"
            )
            assert skill_md.exists(), (
                f"Agent '{agent_name}' → skill '{skill_name}': Missing SKILL.md"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_context_domain_references(self, agent_name, config_path):
        """Check 3: Each configured domain exists under forge-plugin/context/."""
        config = load_json(config_path)
        context_domains = config.get("context", {}).get("domains", [])
        
        for domain in context_domains:
            domain_dir = FORGE_DIR / "context" / domain
            assert domain_dir.is_dir(), (
                f"Agent '{agent_name}' references context domain '{domain}' "
                f"but context/{domain}/ does not exist"
            )
            assert domain in VALID_DOMAINS, (
                f"Agent '{agent_name}' references unknown domain '{domain}'. "
                f"Valid domains: {', '.join(sorted(VALID_DOMAINS))}"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_memory_directory_exists(self, agent_name, config_path):
        """Check 4: Configured memory path exists."""
        config = load_json(config_path)
        memory_config = config.get("memory", {})
        storage_path = memory_config.get("storagePath", "")
        
        if storage_path:
            # Memory paths are relative to forge-plugin/
            memory_dir = FORGE_DIR / storage_path.replace("forge-plugin/", "")
            assert memory_dir.is_dir(), (
                f"Agent '{agent_name}' specifies memory path '{storage_path}' "
                f"but {memory_dir.relative_to(FORGE_DIR.parent)} does not exist"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_personality_file_parity(self, agent_name, config_path):
        """Check 5: Matching {name}.md exists for {name}.config.json."""
        # The .md file should be {name}.md (not {name}.config.md)
        personality_md = config_path.parent / f"{agent_name}.md"
        assert personality_md.exists(), (
            f"Agent '{agent_name}' has config file but missing personality file: "
            f"{agent_name}.md"
        )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_mcp_references_exist(self, agent_name, config_path):
        """Check 6: Referenced MCP docs exist in forge-plugin/mcps/."""
        config = load_json(config_path)
        mcps = config.get("mcps", [])
        
        for mcp_entry in mcps:
            mcp_name = mcp_entry.get("name", "")
            mcp_doc = FORGE_DIR / "mcps" / f"{mcp_name}.md"
            
            assert mcp_doc.exists(), (
                f"Agent '{agent_name}' references MCP '{mcp_name}' "
                f"but mcps/{mcp_name}.md does not exist"
            )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_configs(),
        ids=[name for name, _ in _get_agent_configs()],
    )
    def test_agent_naming_conventions(self, agent_name, config_path):
        """Check 7: File naming follows kebab-case and files match."""
        # Check kebab-case
        assert _is_kebab_case(agent_name), (
            f"Agent name '{agent_name}' does not follow kebab-case convention"
        )
        
        # Check file naming consistency
        config_name = config_path.stem  # Will be "{name}.config"
        # Extract the actual name without .config
        actual_name = config_name.replace('.config', '')
        
        assert actual_name == agent_name, (
            f"Config file name mismatch: expected '{agent_name}.config.json', "
            f"got '{config_path.name}'"
        )
        
        # Check personality file exists and matches
        personality_md = config_path.parent / f"{agent_name}.md"
        if personality_md.exists():
            personality_name = personality_md.stem
            assert personality_name == agent_name, (
                f"Personality file name '{personality_name}.md' does not match '{agent_name}.md'"
            )
