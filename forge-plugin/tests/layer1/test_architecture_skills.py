"""Test Architecture & Design skills — structure, frontmatter, and cross-references.

Validates:
- All 4 Architecture & Design skills have SKILL.md + examples.md
- SKILL.md files have valid YAML frontmatter with required fields
- Memory index files exist at canonical paths
- Interface references use correct patterns (no hardcoded paths)
- Compliance checklists and version history are present
- Workflow steps follow mandatory ordering conventions

Phase 1 of the Forge Testing Architecture.
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

ARCHITECTURE_SKILLS = [
    "api-design",
    "architecture-design",
    "graphql-design",
    "microservices-design",
]

REQUIRED_FRONTMATTER_FIELDS = {"name", "description", "version"}
REQUIRED_FRONTMATTER_CONTEXT_FIELDS = {"primary_domain", "file_budget"}
REQUIRED_FRONTMATTER_MEMORY_FIELDS = {"scopes"}

INTERFACE_REFERENCES = [
    "ContextProvider",
    "MemoryStore",
]

MANDATORY_SECTIONS = [
    "Mandatory Workflow",
    "Compliance Checklist",
    "Version History",
]


# ---------------------------------------------------------------------------
# Skill File Structure Tests
# ---------------------------------------------------------------------------


class TestArchitectureSkillStructure:
    """Validate that all Architecture & Design skills have required files."""

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_skill_directory_exists(self, skill_name):
        """Each architecture skill must have a directory."""
        skill_dir = FORGE_DIR / "skills" / skill_name
        assert skill_dir.is_dir(), (
            f"Skill directory missing: skills/{skill_name}/"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_skill_has_skill_md(self, skill_name):
        """Each architecture skill must have SKILL.md."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        assert skill_md.is_file(), (
            f"Skill '{skill_name}' missing SKILL.md"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_skill_has_examples_md(self, skill_name):
        """Each architecture skill must have examples.md."""
        examples_md = FORGE_DIR / "skills" / skill_name / "examples.md"
        assert examples_md.is_file(), (
            f"Skill '{skill_name}' missing examples.md"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_memory_index_exists(self, skill_name):
        """Each architecture skill must have a memory index file."""
        index_md = FORGE_DIR / "memory" / "skills" / skill_name / "index.md"
        assert index_md.is_file(), (
            f"Memory index missing: memory/skills/{skill_name}/index.md"
        )


# ---------------------------------------------------------------------------
# YAML Frontmatter Tests
# ---------------------------------------------------------------------------


class TestArchitectureSkillFrontmatter:
    """Validate YAML frontmatter in SKILL.md files."""

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_frontmatter_exists(self, skill_name):
        """SKILL.md must have YAML frontmatter."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, (
            f"Skill '{skill_name}' SKILL.md missing YAML frontmatter"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_frontmatter_has_required_fields(self, skill_name):
        """Frontmatter must contain name, description, and version."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, "No frontmatter found"
        for field in REQUIRED_FRONTMATTER_FIELDS:
            assert field in fm, (
                f"Skill '{skill_name}' frontmatter missing '{field}'"
            )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_frontmatter_name_matches_directory(self, skill_name):
        """Frontmatter 'name' must match the skill directory name."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, "No frontmatter found"
        assert fm["name"] == skill_name, (
            f"Frontmatter name '{fm['name']}' does not match directory '{skill_name}'"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_frontmatter_version_format(self, skill_name):
        """Version must follow semver format (X.Y.Z)."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, "No frontmatter found"
        version = fm.get("version", "")
        assert re.match(r"^\d+\.\d+\.\d+", str(version)), (
            f"Skill '{skill_name}' version '{version}' is not valid semver"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_frontmatter_has_context_section(self, skill_name):
        """Frontmatter must have a context section with required fields."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, "No frontmatter found"
        assert "context" in fm, (
            f"Skill '{skill_name}' frontmatter missing 'context' section"
        )
        context = fm["context"]
        for field in REQUIRED_FRONTMATTER_CONTEXT_FIELDS:
            assert field in context, (
                f"Skill '{skill_name}' context section missing '{field}'"
            )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_frontmatter_has_memory_section(self, skill_name):
        """Frontmatter must have a memory section with scopes."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, "No frontmatter found"
        assert "memory" in fm, (
            f"Skill '{skill_name}' frontmatter missing 'memory' section"
        )
        memory = fm["memory"]
        for field in REQUIRED_FRONTMATTER_MEMORY_FIELDS:
            assert field in memory, (
                f"Skill '{skill_name}' memory section missing '{field}'"
            )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_frontmatter_has_tags(self, skill_name):
        """Frontmatter must have tags array with at least 3 tags."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, "No frontmatter found"
        assert "tags" in fm, (
            f"Skill '{skill_name}' frontmatter missing 'tags'"
        )
        tags = fm["tags"]
        assert isinstance(tags, list), (
            f"Skill '{skill_name}' tags must be a list"
        )
        assert len(tags) >= 3, (
            f"Skill '{skill_name}' must have at least 3 tags, found {len(tags)}"
        )


# ---------------------------------------------------------------------------
# Content Validation Tests
# ---------------------------------------------------------------------------


class TestArchitectureSkillContent:
    """Validate SKILL.md content follows conventions."""

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_interface_references_present(self, skill_name):
        """SKILL.md must reference ContextProvider and MemoryStore interfaces."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        for ref in INTERFACE_REFERENCES:
            assert ref in content, (
                f"Skill '{skill_name}' missing interface reference: {ref}"
            )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_mandatory_sections_present(self, skill_name):
        """SKILL.md must contain Mandatory Workflow, Compliance Checklist, Version History."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8").lower()
        for section in MANDATORY_SECTIONS:
            assert section.lower() in content, (
                f"Skill '{skill_name}' missing section: {section}"
            )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_no_hardcoded_filesystem_paths(self, skill_name):
        """SKILL.md must not contain hardcoded absolute filesystem paths."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        # Check for absolute paths that suggest hardcoded filesystem references
        hardcoded_patterns = [
            r"/home/\w+/",
            r"C:\\Users\\",
            r"/Users/\w+/",
        ]
        for pattern in hardcoded_patterns:
            matches = re.findall(pattern, content)
            assert len(matches) == 0, (
                f"Skill '{skill_name}' contains hardcoded path: {matches}"
            )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_memory_store_usage(self, skill_name):
        """SKILL.md must reference memoryStore for memory operations."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "memoryStore" in content, (
            f"Skill '{skill_name}' does not reference memoryStore interface"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_output_convention_reference(self, skill_name):
        """SKILL.md must reference the output conventions for report routing."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "/claudedocs/" in content, (
            f"Skill '{skill_name}' does not reference /claudedocs/ output directory"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_workflow_steps_ordered(self, skill_name):
        """SKILL.md must have numbered workflow steps in ascending order."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        step_numbers = re.findall(r"###\s+Step\s+(\d+)", content)
        assert len(step_numbers) >= 5, (
            f"Skill '{skill_name}' must have at least 5 workflow steps, found {len(step_numbers)}"
        )
        # Verify steps are in ascending order
        int_steps = [int(s) for s in step_numbers]
        assert int_steps == sorted(int_steps), (
            f"Skill '{skill_name}' workflow steps are not in order: {int_steps}"
        )


# ---------------------------------------------------------------------------
# Examples Validation Tests
# ---------------------------------------------------------------------------


class TestArchitectureSkillExamples:
    """Validate examples.md files follow conventions."""

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_examples_has_minimum_scenarios(self, skill_name):
        """examples.md must contain at least 3 distinct examples."""
        examples_md = FORGE_DIR / "skills" / skill_name / "examples.md"
        content = examples_md.read_text(encoding="utf-8")
        example_count = len(re.findall(r"##\s+Example\s+\d+", content))
        assert example_count >= 3, (
            f"Skill '{skill_name}' examples.md has {example_count} examples, need at least 3"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_examples_have_scenarios(self, skill_name):
        """Each example must have a Scenario section."""
        examples_md = FORGE_DIR / "skills" / skill_name / "examples.md"
        content = examples_md.read_text(encoding="utf-8")
        scenario_count = len(re.findall(r"###\s+Scenario", content))
        example_count = len(re.findall(r"##\s+Example\s+\d+", content))
        assert scenario_count >= example_count, (
            f"Skill '{skill_name}' examples missing Scenario sections "
            f"({scenario_count} scenarios for {example_count} examples)"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_examples_have_user_prompts(self, skill_name):
        """Each example must include a User Prompt."""
        examples_md = FORGE_DIR / "skills" / skill_name / "examples.md"
        content = examples_md.read_text(encoding="utf-8")
        prompt_count = len(re.findall(r"###\s+User Prompt", content))
        assert prompt_count >= 3, (
            f"Skill '{skill_name}' examples has {prompt_count} User Prompts, need at least 3"
        )


# ---------------------------------------------------------------------------
# Memory Index Validation Tests
# ---------------------------------------------------------------------------


class TestArchitectureSkillMemory:
    """Validate memory index files follow conventions."""

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_memory_index_references_skill(self, skill_name):
        """Memory index must reference the parent skill."""
        index_md = FORGE_DIR / "memory" / "skills" / skill_name / "index.md"
        content = index_md.read_text(encoding="utf-8")
        assert skill_name in content, (
            f"Memory index for '{skill_name}' does not reference the skill name"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_memory_index_has_purpose(self, skill_name):
        """Memory index must have a Purpose section."""
        index_md = FORGE_DIR / "memory" / "skills" / skill_name / "index.md"
        content = index_md.read_text(encoding="utf-8")
        assert "## Purpose" in content, (
            f"Memory index for '{skill_name}' missing Purpose section"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_memory_index_has_file_definitions(self, skill_name):
        """Memory index must define required memory files."""
        index_md = FORGE_DIR / "memory" / "skills" / skill_name / "index.md"
        content = index_md.read_text(encoding="utf-8")
        assert "project_overview.md" in content, (
            f"Memory index for '{skill_name}' missing project_overview.md definition"
        )


# ---------------------------------------------------------------------------
# Cross-Reference Tests
# ---------------------------------------------------------------------------


class TestArchitectureSkillCrossReferences:
    """Validate cross-references between skill files are consistent."""

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_skill_references_shared_loading_patterns(self, skill_name):
        """SKILL.md must reference shared loading patterns."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "shared_loading_patterns" in content.lower() or "Shared Loading Patterns" in content, (
            f"Skill '{skill_name}' missing reference to shared loading patterns"
        )

    @pytest.mark.parametrize("skill_name", ARCHITECTURE_SKILLS)
    def test_skill_context_domain_is_engineering(self, skill_name):
        """All architecture skills should use the engineering context domain."""
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, "No frontmatter found"
        assert fm.get("context", {}).get("primary_domain") == "engineering", (
            f"Skill '{skill_name}' should use 'engineering' as primary domain"
        )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
