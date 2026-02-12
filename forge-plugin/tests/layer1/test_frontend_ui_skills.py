"""Test Frontend & UI skills structure, content, and conventions.

Validates:
- All 6 Frontend & UI skills have required files (SKILL.md, examples.md)
- YAML frontmatter has required fields (name, version, description, context, memory, tags)
- SKILL.md contains mandatory workflow steps and compliance checklist
- Interface references are present (ContextProvider, MemoryStore)
- Memory index files exist for each skill
- No hardcoded filesystem paths in skill definitions
- examples.md contains at least 3 usage scenarios

Phase 1 of the Forge Testing Architecture — Frontend & UI skills.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, extract_yaml_frontmatter


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FRONTEND_UI_SKILLS = [
    "accessibility",
    "animate",
    "nextjs",
    "react-forms",
    "responsive-images",
    "tailwind-patterns",
]

SKILLS_DIR = FORGE_DIR / "skills"
MEMORY_DIR = FORGE_DIR / "memory" / "skills"

REQUIRED_FRONTMATTER_FIELDS = ["name", "version", "description", "context", "memory", "tags"]

# Patterns that indicate hardcoded paths (should use interface references instead)
HARDCODED_PATH_PATTERNS = [
    re.compile(r"forge-plugin/context/[a-z]+/[a-z_]+\.md"),
    re.compile(r"forge-plugin/memory/skills/[a-z-]+/[a-z_]+\.md"),
    re.compile(r"\.\./\.\./context/"),
    re.compile(r"\.\./\.\./memory/"),
]

# Allowed path references (documentation, not operational)
ALLOWED_PATH_REFS = [
    "../../interfaces/",
    "../OUTPUT_CONVENTIONS.md",
    "../../interfaces/shared_loading_patterns.md",
    "../../interfaces/context_provider.md",
    "../../interfaces/memory_store.md",
    "../../interfaces/schemas/",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _skill_dir(skill_name: str) -> Path:
    return SKILLS_DIR / skill_name


def _skill_md(skill_name: str) -> Path:
    return SKILLS_DIR / skill_name / "SKILL.md"


def _examples_md(skill_name: str) -> Path:
    return SKILLS_DIR / skill_name / "examples.md"


def _memory_index(skill_name: str) -> Path:
    return MEMORY_DIR / skill_name / "index.md"


# ---------------------------------------------------------------------------
# File Structure Tests
# ---------------------------------------------------------------------------


class TestFrontendUISkillStructure:
    """Validate all 6 Frontend & UI skills have required files."""

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_skill_directory_exists(self, skill):
        """Each Frontend & UI skill must have a directory."""
        assert _skill_dir(skill).is_dir(), (
            f"Skill directory missing: skills/{skill}/"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_skill_md_exists(self, skill):
        """Each skill must have SKILL.md."""
        assert _skill_md(skill).is_file(), (
            f"Skill file missing: skills/{skill}/SKILL.md"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_examples_md_exists(self, skill):
        """Each skill must have examples.md."""
        assert _examples_md(skill).is_file(), (
            f"Examples file missing: skills/{skill}/examples.md"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_memory_index_exists(self, skill):
        """Each skill must have a memory index file."""
        assert _memory_index(skill).is_file(), (
            f"Memory index missing: memory/skills/{skill}/index.md"
        )


# ---------------------------------------------------------------------------
# YAML Frontmatter Tests
# ---------------------------------------------------------------------------


class TestFrontendUIFrontmatter:
    """Validate YAML frontmatter in all SKILL.md files."""

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_frontmatter(self, skill):
        """SKILL.md must have YAML frontmatter."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        assert fm is not None, (
            f"skills/{skill}/SKILL.md: No YAML frontmatter found"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_required_fields(self, skill):
        """Frontmatter must have all required fields."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        if fm is None:
            pytest.skip("No frontmatter")
        missing = [f for f in REQUIRED_FRONTMATTER_FIELDS if f not in fm]
        assert not missing, (
            f"skills/{skill}/SKILL.md: Missing frontmatter fields: {missing}"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_name_matches_directory(self, skill):
        """Frontmatter name must match directory name."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        if fm is None:
            pytest.skip("No frontmatter")
        assert fm.get("name") == skill, (
            f"skills/{skill}/SKILL.md: name='{fm.get('name')}' doesn't match dir '{skill}'"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_version_is_1_0_0(self, skill):
        """Version must be 1.0.0 for initial release."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        if fm is None:
            pytest.skip("No frontmatter")
        assert fm.get("version") == "1.0.0", (
            f"skills/{skill}/SKILL.md: version='{fm.get('version')}', expected '1.0.0'"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_description_not_empty(self, skill):
        """Description must not be empty."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        if fm is None:
            pytest.skip("No frontmatter")
        desc = fm.get("description", "")
        assert len(desc) > 20, (
            f"skills/{skill}/SKILL.md: description too short ({len(desc)} chars)"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_tags_present_and_populated(self, skill):
        """Tags must be a non-empty list."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        if fm is None:
            pytest.skip("No frontmatter")
        tags = fm.get("tags", [])
        assert isinstance(tags, list), (
            f"skills/{skill}/SKILL.md: tags must be a list"
        )
        assert len(tags) >= 3, (
            f"skills/{skill}/SKILL.md: tags should have at least 3 entries, got {len(tags)}"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_context_has_primary_domain(self, skill):
        """Context must specify a primary_domain."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        if fm is None:
            pytest.skip("No frontmatter")
        context = fm.get("context", {})
        assert "primary_domain" in context, (
            f"skills/{skill}/SKILL.md: context missing primary_domain"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_memory_has_scopes(self, skill):
        """Memory must define scopes."""
        fm = extract_yaml_frontmatter(_skill_md(skill))
        if fm is None:
            pytest.skip("No frontmatter")
        memory = fm.get("memory", {})
        assert "scopes" in memory, (
            f"skills/{skill}/SKILL.md: memory missing scopes"
        )
        scopes = memory["scopes"]
        assert isinstance(scopes, list) and len(scopes) > 0, (
            f"skills/{skill}/SKILL.md: memory.scopes must be a non-empty list"
        )


# ---------------------------------------------------------------------------
# Content Structure Tests
# ---------------------------------------------------------------------------


class TestFrontendUISkillContent:
    """Validate SKILL.md content structure and conventions."""

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_mandatory_workflow(self, skill):
        """SKILL.md must contain mandatory workflow section."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "MANDATORY WORKFLOW" in content or "Mandatory Workflow" in content, (
            f"skills/{skill}/SKILL.md: Missing mandatory workflow section"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_compliance_checklist(self, skill):
        """SKILL.md must contain a compliance checklist."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "Compliance Checklist" in content, (
            f"skills/{skill}/SKILL.md: Missing compliance checklist"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_version_history(self, skill):
        """SKILL.md must contain version history."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "Version History" in content, (
            f"skills/{skill}/SKILL.md: Missing version history section"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_interface_references(self, skill):
        """SKILL.md must reference ContextProvider and MemoryStore interfaces."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "ContextProvider" in content or "contextProvider" in content, (
            f"skills/{skill}/SKILL.md: Missing ContextProvider reference"
        )
        assert "MemoryStore" in content or "memoryStore" in content, (
            f"skills/{skill}/SKILL.md: Missing MemoryStore reference"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_memory_loading_step(self, skill):
        """SKILL.md must include a memory loading step."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "Load Memory" in content or "memoryStore.getSkillMemory" in content, (
            f"skills/{skill}/SKILL.md: Missing memory loading step"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_context_loading_step(self, skill):
        """SKILL.md must include a context loading step."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "Load Context" in content or "contextProvider" in content, (
            f"skills/{skill}/SKILL.md: Missing context loading step"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_output_step(self, skill):
        """SKILL.md must include an output generation step."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "Generate Output" in content or "/claudedocs/" in content, (
            f"skills/{skill}/SKILL.md: Missing output generation step"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_memory_update_step(self, skill):
        """SKILL.md must include a memory update step."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "Update Memory" in content or "memoryStore.update" in content, (
            f"skills/{skill}/SKILL.md: Missing memory update step"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_references_shared_loading_patterns(self, skill):
        """SKILL.md must reference shared loading patterns."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        assert "shared_loading_patterns" in content or "Standard Memory Loading" in content, (
            f"skills/{skill}/SKILL.md: Missing shared loading patterns reference"
        )


# ---------------------------------------------------------------------------
# Examples Tests
# ---------------------------------------------------------------------------


class TestFrontendUIExamples:
    """Validate examples.md content."""

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_has_at_least_3_examples(self, skill):
        """examples.md must contain at least 3 usage scenarios."""
        content = _examples_md(skill).read_text(encoding="utf-8")
        # Count ## Example or ## Scenario headers
        example_count = len(re.findall(r"^## Example \d", content, re.MULTILINE))
        assert example_count >= 3, (
            f"skills/{skill}/examples.md: Found {example_count} examples, need at least 3"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_examples_have_code_blocks(self, skill):
        """examples.md must contain code examples."""
        content = _examples_md(skill).read_text(encoding="utf-8")
        code_blocks = len(re.findall(r"```\w+", content))
        assert code_blocks >= 3, (
            f"skills/{skill}/examples.md: Found {code_blocks} code blocks, need at least 3"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_examples_not_empty(self, skill):
        """examples.md must have substantial content."""
        content = _examples_md(skill).read_text(encoding="utf-8")
        assert len(content) > 500, (
            f"skills/{skill}/examples.md: Content too short ({len(content)} chars)"
        )


# ---------------------------------------------------------------------------
# Memory Structure Tests
# ---------------------------------------------------------------------------


class TestFrontendUIMemory:
    """Validate memory index files."""

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_memory_dir_exists(self, skill):
        """Memory directory must exist for each skill."""
        assert (MEMORY_DIR / skill).is_dir(), (
            f"Memory directory missing: memory/skills/{skill}/"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_memory_index_references_skill(self, skill):
        """Memory index must reference the parent skill."""
        content = _memory_index(skill).read_text(encoding="utf-8")
        assert skill in content, (
            f"memory/skills/{skill}/index.md: Does not reference skill name '{skill}'"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_memory_index_has_purpose(self, skill):
        """Memory index must have a Purpose section."""
        content = _memory_index(skill).read_text(encoding="utf-8")
        assert "## Purpose" in content, (
            f"memory/skills/{skill}/index.md: Missing Purpose section"
        )

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_memory_index_has_file_descriptions(self, skill):
        """Memory index must describe memory files."""
        content = _memory_index(skill).read_text(encoding="utf-8")
        assert "project_overview" in content or "project_overview.md" in content, (
            f"memory/skills/{skill}/index.md: Missing project_overview file description"
        )
        assert "common_patterns" in content or "common_patterns.md" in content, (
            f"memory/skills/{skill}/index.md: Missing common_patterns file description"
        )


# ---------------------------------------------------------------------------
# No Hardcoded Paths Tests
# ---------------------------------------------------------------------------


class TestNoHardcodedPaths:
    """Ensure SKILL.md files use interface references, not hardcoded paths."""

    @pytest.mark.parametrize("skill", FRONTEND_UI_SKILLS)
    def test_no_hardcoded_context_paths(self, skill):
        """SKILL.md must not contain hardcoded context file paths."""
        content = _skill_md(skill).read_text(encoding="utf-8")
        for pattern in HARDCODED_PATH_PATTERNS:
            matches = pattern.findall(content)
            # Filter out allowed references (interface docs)
            real_violations = [
                m for m in matches
                if not any(allowed in m for allowed in ALLOWED_PATH_REFS)
            ]
            assert not real_violations, (
                f"skills/{skill}/SKILL.md: Hardcoded path found: {real_violations}. "
                f"Use interface references instead."
            )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
