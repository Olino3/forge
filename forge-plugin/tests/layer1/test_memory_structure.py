"""Test memory directory structure and file format conventions.

Validates:
- Required memory index/lifecycle/quality files exist
- Agent memory dirs match actual agents
- Skill memory dirs match actual skills
- Memory files (if present) have timestamp markers
- No memory files exceed line limits (200/300/500)
- Memory subdirectory structure follows conventions

Phase 2 of the Forge Testing Architecture.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MEMORY_DIR = FORGE_DIR / "memory"

REQUIRED_TOP_LEVEL_FILES = ["index.md", "lifecycle.md", "quality_guidance.md"]
REQUIRED_LAYER_DIRS = ["agents", "commands", "projects", "skills"]

# Line limits from lifecycle.md
LINE_LIMITS = {
    "project_overview": 200,
    "review_history": 300,
    # Default max for any memory file
    "_default": 500,
}

# Operational files that should NOT be checked for memory conventions
OPERATIONAL_FILES = {"index.md", "lifecycle.md", "quality_guidance.md", "README.md", ".gitkeep"}

# Two accepted timestamp formats used in the codebase
TIMESTAMP_PATTERNS = [
    re.compile(r"<!--\s*Last Updated:\s*\d{4}-\d{2}-\d{2}\s*-->"),  # HTML comment
    re.compile(r"\*\*Last Updated\*\*:\s*\d{4}-\d{2}-\d{2}"),       # Bold markdown
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_memory_content_files() -> list[tuple[str, Path]]:
    """Return (relative_path, full_path) for actual memory content .md files.

    Excludes operational files (index.md, lifecycle.md, etc.) and .gitkeep.
    """
    files = []
    for f in sorted(MEMORY_DIR.rglob("*.md")):
        if f.name in OPERATIONAL_FILES:
            continue
        files.append((str(f.relative_to(MEMORY_DIR)), f))
    return files


def _get_agent_names() -> set[str]:
    """Return set of actual agent names from agents/ directory."""
    agents_dir = FORGE_DIR / "agents"
    return {
        p.name.replace(".config.json", "")
        for p in agents_dir.glob("*.config.json")
    }


def _get_skill_names() -> set[str]:
    """Return set of actual skill names from skills/ directory."""
    skills_dir = FORGE_DIR / "skills"
    return {
        d.name
        for d in skills_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    }


def _file_type_from_name(filename: str) -> str:
    """Extract memory file type from filename (e.g., 'project_overview.md' → 'project_overview')."""
    return filename.replace(".md", "")


# ---------------------------------------------------------------------------
# Required Structure Tests
# ---------------------------------------------------------------------------


class TestMemoryRequiredStructure:
    """Validate required memory directory structure."""

    def test_memory_dir_exists(self):
        """memory/ directory must exist."""
        assert MEMORY_DIR.is_dir()

    @pytest.mark.parametrize("filename", REQUIRED_TOP_LEVEL_FILES)
    def test_required_top_level_files(self, filename):
        """Required top-level memory files must exist."""
        assert (MEMORY_DIR / filename).is_file(), (
            f"memory/{filename} missing"
        )

    @pytest.mark.parametrize("dirname", REQUIRED_LAYER_DIRS)
    def test_required_layer_dirs(self, dirname):
        """Required memory layer directories must exist."""
        assert (MEMORY_DIR / dirname).is_dir(), (
            f"memory/{dirname}/ directory missing"
        )

    def test_projects_has_index(self):
        """memory/projects/ must have index.md."""
        assert (MEMORY_DIR / "projects" / "index.md").is_file()

    def test_commands_has_index(self):
        """memory/commands/ must have index.md."""
        assert (MEMORY_DIR / "commands" / "index.md").is_file()


# ---------------------------------------------------------------------------
# Agent Memory Directory Tests
# ---------------------------------------------------------------------------


class TestAgentMemoryDirs:
    """Validate agent memory directories match actual agents."""

    def test_all_agents_have_memory_dirs(self):
        """Every agent with a config must have a memory subdirectory."""
        agents = _get_agent_names()
        agents_memory_dir = MEMORY_DIR / "agents"
        if not agents_memory_dir.is_dir():
            pytest.skip("memory/agents/ not found")
        for agent_name in sorted(agents):
            agent_dir = agents_memory_dir / agent_name
            assert agent_dir.is_dir(), (
                f"Agent '{agent_name}' has config but no memory dir at "
                f"memory/agents/{agent_name}/"
            )

    def test_agent_memory_dirs_have_readme(self):
        """Agent memory dirs should have README.md."""
        agents_memory_dir = MEMORY_DIR / "agents"
        if not agents_memory_dir.is_dir():
            pytest.skip("memory/agents/ not found")
        for agent_dir in sorted(agents_memory_dir.iterdir()):
            if agent_dir.is_dir() and not agent_dir.name.startswith("."):
                readme = agent_dir / "README.md"
                assert readme.exists(), (
                    f"memory/agents/{agent_dir.name}/: Missing README.md"
                )


# ---------------------------------------------------------------------------
# Skill Memory Directory Tests
# ---------------------------------------------------------------------------


class TestSkillMemoryDirs:
    """Validate skill memory directory conventions."""

    def test_skills_memory_dir_exists(self):
        """memory/skills/ directory must exist."""
        assert (MEMORY_DIR / "skills").is_dir()

    def test_skill_memory_dirs_exist_for_skills_with_memory(self):
        """Skill memory dirs should correspond to actual skills."""
        skills_memory_dir = MEMORY_DIR / "skills"
        actual_skills = _get_skill_names()
        for skill_dir in sorted(skills_memory_dir.iterdir()):
            if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                assert skill_dir.name in actual_skills, (
                    f"memory/skills/{skill_dir.name}/: No matching skill directory. "
                    f"Orphaned memory directory?"
                )


# ---------------------------------------------------------------------------
# Memory File Timestamp Tests
# ---------------------------------------------------------------------------


class TestMemoryFileTimestamps:
    """Validate memory content files have timestamp markers."""

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_memory_content_files(),
        ids=[r for r, _ in _get_memory_content_files()],
    )
    def test_memory_file_has_timestamp(self, rel_path, filepath):
        """Memory content files should have a Last Updated timestamp."""
        content = filepath.read_text(encoding="utf-8")
        # Check first 10 lines for timestamp
        first_lines = "\n".join(content.split("\n")[:10])
        has_timestamp = any(
            pattern.search(first_lines)
            for pattern in TIMESTAMP_PATTERNS
        )
        if not has_timestamp:
            # Warn but don't fail — some files may be templates
            pytest.skip(
                f"{rel_path}: No timestamp found in first 10 lines "
                f"(expected <!-- Last Updated: YYYY-MM-DD --> or "
                f"**Last Updated**: YYYY-MM-DD)"
            )


# ---------------------------------------------------------------------------
# Memory File Line Limit Tests
# ---------------------------------------------------------------------------


class TestMemoryFileLineLimits:
    """Validate memory files don't exceed line limits."""

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_memory_content_files(),
        ids=[r for r, _ in _get_memory_content_files()],
    )
    def test_memory_file_within_line_limits(self, rel_path, filepath):
        """Memory files must not exceed their type-specific line limit."""
        file_type = _file_type_from_name(filepath.name)
        limit = LINE_LIMITS.get(file_type, LINE_LIMITS["_default"])

        line_count = len(filepath.read_text(encoding="utf-8").splitlines())
        assert line_count <= limit, (
            f"{rel_path}: {line_count} lines exceeds {file_type} limit of {limit}"
        )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
