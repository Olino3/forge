"""Test file structure conventions for the Forge plugin.

Validates:
- All required directories from root_safety_profile.json exist
- All required files from root_safety_profile.json exist
- Each agent has paired .md + .config.json files
- Each skill directory has SKILL.md + examples.md
- Each command directory has COMMAND.md
- Memory layer subdirectories exist (agents, commands, projects, skills)
- Context domain directories match valid domain set

Phase 1 of the Forge Testing Architecture.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, REPO_ROOT, load_json


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EXPECTED_MEMORY_SUBDIRS = {"agents", "commands", "projects", "skills"}

CONTEXT_DOMAIN_DIRS = {
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


# ---------------------------------------------------------------------------
# Required Structure Tests (from root_safety_profile.json)
# ---------------------------------------------------------------------------


class TestRequiredStructure:
    """Validate directories and files declared in root_safety_profile.json."""

    @pytest.fixture(scope="class")
    def safety_profile(self):
        safety_path = FORGE_DIR / "templates" / "root_safety_profile.json"
        assert safety_path.exists(), "root_safety_profile.json not found"
        return load_json(safety_path)

    @pytest.fixture(scope="class")
    def required_dirs(self, safety_profile):
        return safety_profile.get("requiredStructure", {}).get("directories", [])

    @pytest.fixture(scope="class")
    def required_files(self, safety_profile):
        return safety_profile.get("requiredStructure", {}).get("files", [])

    def test_required_directories_exist(self, required_dirs):
        """All directories declared in requiredStructure must exist."""
        for dir_rel in required_dirs:
            dir_path = REPO_ROOT / dir_rel
            assert dir_path.is_dir(), (
                f"Required directory missing: {dir_rel}"
            )

    def test_required_files_exist(self, required_files):
        """All files declared in requiredStructure must exist."""
        for file_rel in required_files:
            file_path = REPO_ROOT / file_rel
            assert file_path.is_file(), (
                f"Required file missing: {file_rel}"
            )


# ---------------------------------------------------------------------------
# Agent Pairing Tests
# ---------------------------------------------------------------------------


class TestAgentPairing:
    """Validate that every agent has both .md and .config.json files."""

    @pytest.fixture(scope="class")
    def agents_dir(self):
        d = FORGE_DIR / "agents"
        assert d.is_dir(), "agents/ directory not found"
        return d

    def test_every_config_has_markdown(self, agents_dir):
        """Every *.config.json must have a matching *.md."""
        configs = sorted(agents_dir.glob("*.config.json"))
        assert len(configs) > 0, "No agent config files found"
        for config_path in configs:
            agent_name = config_path.name.replace(".config.json", "")
            md_path = agents_dir / f"{agent_name}.md"
            assert md_path.exists(), (
                f"Agent '{agent_name}' has config but missing {agent_name}.md"
            )

    def test_every_markdown_has_config(self, agents_dir):
        """Every agent *.md must have a matching *.config.json."""
        markdowns = sorted(agents_dir.glob("*.md"))
        assert len(markdowns) > 0, "No agent markdown files found"
        for md_path in markdowns:
            agent_name = md_path.stem
            config_path = agents_dir / f"{agent_name}.config.json"
            assert config_path.exists(), (
                f"Agent '{agent_name}' has markdown but missing {agent_name}.config.json"
            )


# ---------------------------------------------------------------------------
# Skill Structure Tests
# ---------------------------------------------------------------------------


def _get_skill_dirs() -> list[Path]:
    """Return all skill directories (exclude top-level non-dir files)."""
    skills_dir = FORGE_DIR / "skills"
    return sorted(
        d for d in skills_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


class TestSkillStructure:
    """Validate skill directory conventions."""

    def test_skills_exist(self):
        """At least one skill directory must exist."""
        assert len(_get_skill_dirs()) > 0, "No skill directories found"

    @pytest.mark.parametrize(
        "skill_dir",
        _get_skill_dirs(),
        ids=[d.name for d in _get_skill_dirs()],
    )
    def test_skill_has_skill_md(self, skill_dir):
        """Every skill directory must contain SKILL.md."""
        skill_md = skill_dir / "SKILL.md"
        assert skill_md.exists(), (
            f"Skill '{skill_dir.name}' missing SKILL.md"
        )

    @pytest.mark.parametrize(
        "skill_dir",
        _get_skill_dirs(),
        ids=[d.name for d in _get_skill_dirs()],
    )
    def test_skill_has_examples_md(self, skill_dir):
        """Every skill directory must contain examples.md."""
        examples_md = skill_dir / "examples.md"
        assert examples_md.exists(), (
            f"Skill '{skill_dir.name}' missing examples.md"
        )


# ---------------------------------------------------------------------------
# Command Structure Tests
# ---------------------------------------------------------------------------


def _get_command_dirs() -> list[Path]:
    """Return all command directories (exclude top-level files like index.md)."""
    commands_dir = FORGE_DIR / "commands"
    return sorted(
        d for d in commands_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


class TestCommandStructure:
    """Validate command directory conventions."""

    def test_commands_exist(self):
        """At least one command directory must exist."""
        assert len(_get_command_dirs()) > 0, "No command directories found"

    @pytest.mark.parametrize(
        "cmd_dir",
        _get_command_dirs(),
        ids=[d.name for d in _get_command_dirs()],
    )
    def test_command_has_command_md(self, cmd_dir):
        """Every command directory must contain COMMAND.md."""
        command_md = cmd_dir / "COMMAND.md"
        assert command_md.exists(), (
            f"Command '{cmd_dir.name}' missing COMMAND.md"
        )


# ---------------------------------------------------------------------------
# Memory Structure Tests
# ---------------------------------------------------------------------------


class TestMemoryStructure:
    """Validate memory directory conventions."""

    def test_memory_dir_exists(self):
        """memory/ directory must exist."""
        assert (FORGE_DIR / "memory").is_dir(), "memory/ directory not found"

    def test_memory_has_index(self):
        """memory/ must have an index.md."""
        assert (FORGE_DIR / "memory" / "index.md").is_file(), (
            "memory/index.md missing"
        )

    @pytest.mark.parametrize("subdir", sorted(EXPECTED_MEMORY_SUBDIRS))
    def test_memory_layer_subdirs_exist(self, subdir):
        """Memory must have the four layer subdirs: agents, commands, projects, skills."""
        path = FORGE_DIR / "memory" / subdir
        assert path.is_dir(), f"memory/{subdir}/ directory missing"


# ---------------------------------------------------------------------------
# Context Domain Tests
# ---------------------------------------------------------------------------


class TestContextStructure:
    """Validate context domain directories."""

    def test_context_dir_exists(self):
        """context/ directory must exist."""
        assert (FORGE_DIR / "context").is_dir(), "context/ directory not found"

    def test_context_has_index(self):
        """context/ must have an index.md."""
        assert (FORGE_DIR / "context" / "index.md").is_file(), (
            "context/index.md missing"
        )

    @pytest.mark.parametrize("domain", sorted(CONTEXT_DOMAIN_DIRS))
    def test_context_domain_dirs_exist(self, domain):
        """Each valid domain must have a context subdirectory."""
        path = FORGE_DIR / "context" / domain
        assert path.is_dir(), f"context/{domain}/ directory missing"


# ---------------------------------------------------------------------------
# Interface Files Tests
# ---------------------------------------------------------------------------


class TestInterfaceStructure:
    """Validate core interface files exist."""

    REQUIRED_INTERFACES = [
        "context_provider.md",
        "memory_store.md",
        "skill_invoker.md",
        "execution_context.md",
    ]

    @pytest.mark.parametrize("filename", REQUIRED_INTERFACES)
    def test_interface_files_exist(self, filename):
        """Core interface definition files must exist."""
        path = FORGE_DIR / "interfaces" / filename
        assert path.is_file(), f"interfaces/{filename} missing"

    def test_schemas_directory_exists(self):
        """interfaces/schemas/ directory must exist."""
        assert (FORGE_DIR / "interfaces" / "schemas").is_dir()

    def test_adapters_directory_exists(self):
        """interfaces/adapters/ directory must exist."""
        assert (FORGE_DIR / "interfaces" / "adapters").is_dir()


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
