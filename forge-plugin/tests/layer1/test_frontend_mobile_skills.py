"""Test Frontend & Mobile skills — structure, frontmatter, and interface compliance.

Validates:
- All 6 Frontend & Mobile skills have SKILL.md + examples.md
- YAML frontmatter contains required fields (name, version, description, context, memory, tags)
- No hardcoded filesystem paths in SKILL.md (uses interface references)
- Memory index exists for each skill
- Memory index follows conventions (has Version and Last Updated)
- Skill workflow includes mandatory steps (Initial Analysis, Load Memory, Load Context, Generate Output, Update Memory)
- Examples contain at least 3 scenarios
- Interface references section present in SKILL.md

Phase 1+ of the Forge Testing Architecture — Frontend & Mobile skills.
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

FRONTEND_MOBILE_SKILLS = [
    "angular-architect",
    "flutter-expert",
    "react-expert",
    "react-native-expert",
    "vue-expert-js",
    "vue-expert",
]

SKILLS_DIR = FORGE_DIR / "skills"
MEMORY_DIR = FORGE_DIR / "memory" / "skills"

REQUIRED_FRONTMATTER_FIELDS = ["name", "version", "description", "context", "memory", "tags"]

MANDATORY_WORKFLOW_KEYWORDS = [
    "Initial Analysis",
    "Load Memory",
    "Load Context",
    "Generate Output",
    "Update Memory",
]

HARDCODED_PATH_PATTERNS = [
    re.compile(r"(?<!\[)(?<!\()../../context/[a-z]+/[a-z_]+\.md(?!\))"),
    re.compile(r"(?<!\[)(?<!\()../../memory/[a-z]+/[a-z_]+\.md(?!\))"),
]

INTERFACE_REFERENCE_PATTERNS = [
    re.compile(r"contextProvider"),
    re.compile(r"memoryStore"),
    re.compile(r"ContextProvider"),
    re.compile(r"MemoryStore"),
]


# ---------------------------------------------------------------------------
# Skill Directory Structure Tests
# ---------------------------------------------------------------------------


class TestFrontendMobileSkillStructure:
    """Validate all Frontend & Mobile skill directories exist with required files."""

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_skill_directory_exists(self, skill_name):
        """Skill directory must exist."""
        skill_dir = SKILLS_DIR / skill_name
        assert skill_dir.is_dir(), (
            f"Skill directory missing: skills/{skill_name}/"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_skill_has_skill_md(self, skill_name):
        """Every skill must have SKILL.md."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        assert skill_md.is_file(), (
            f"skills/{skill_name}/SKILL.md missing"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_skill_has_examples_md(self, skill_name):
        """Every skill must have examples.md."""
        examples_md = SKILLS_DIR / skill_name / "examples.md"
        assert examples_md.is_file(), (
            f"skills/{skill_name}/examples.md missing"
        )


# ---------------------------------------------------------------------------
# YAML Frontmatter Tests
# ---------------------------------------------------------------------------


class TestFrontendMobileFrontmatter:
    """Validate YAML frontmatter in all Frontend & Mobile SKILL.md files."""

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_skill_has_frontmatter(self, skill_name):
        """SKILL.md must have YAML frontmatter."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        assert fm is not None, (
            f"skills/{skill_name}/SKILL.md: No YAML frontmatter found"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_frontmatter_has_required_fields(self, skill_name):
        """Frontmatter must contain all required fields."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        if fm is None:
            pytest.skip("No frontmatter")
        missing = [f for f in REQUIRED_FRONTMATTER_FIELDS if f not in fm]
        assert not missing, (
            f"skills/{skill_name}/SKILL.md: Missing frontmatter fields: {missing}"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_frontmatter_name_matches_directory(self, skill_name):
        """Frontmatter name field must match the skill directory name."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        if fm is None:
            pytest.skip("No frontmatter")
        assert fm.get("name") == skill_name, (
            f"skills/{skill_name}/SKILL.md: name='{fm.get('name')}' "
            f"doesn't match directory '{skill_name}'"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_frontmatter_version_is_valid(self, skill_name):
        """Version must be a valid semver string."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        if fm is None:
            pytest.skip("No frontmatter")
        version = fm.get("version", "")
        assert re.match(r"^\d+\.\d+\.\d+", str(version)), (
            f"skills/{skill_name}/SKILL.md: version '{version}' is not valid semver"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_frontmatter_tags_is_list(self, skill_name):
        """Tags must be a non-empty list."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        if fm is None:
            pytest.skip("No frontmatter")
        tags = fm.get("tags")
        assert isinstance(tags, list) and len(tags) > 0, (
            f"skills/{skill_name}/SKILL.md: tags must be a non-empty list"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_frontmatter_context_has_primary_domain(self, skill_name):
        """Context must declare a primary_domain."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        if fm is None:
            pytest.skip("No frontmatter")
        context = fm.get("context", {})
        assert "primary_domain" in context, (
            f"skills/{skill_name}/SKILL.md: context missing 'primary_domain'"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_frontmatter_memory_has_scopes(self, skill_name):
        """Memory must declare scopes with files."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        if fm is None:
            pytest.skip("No frontmatter")
        memory = fm.get("memory", {})
        scopes = memory.get("scopes", [])
        assert len(scopes) > 0, (
            f"skills/{skill_name}/SKILL.md: memory must declare at least one scope"
        )
        skill_scope = next((s for s in scopes if s.get("type") == "skill-specific"), None)
        assert skill_scope is not None, (
            f"skills/{skill_name}/SKILL.md: memory must have a 'skill-specific' scope"
        )
        assert len(skill_scope.get("files", [])) > 0, (
            f"skills/{skill_name}/SKILL.md: skill-specific scope must declare files"
        )


# ---------------------------------------------------------------------------
# Interface Compliance Tests
# ---------------------------------------------------------------------------


class TestFrontendMobileInterfaceCompliance:
    """Validate skills use interface references and avoid hardcoded paths."""

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_no_hardcoded_context_paths(self, skill_name):
        """SKILL.md must not contain hardcoded context file paths in prose."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        for pattern in HARDCODED_PATH_PATTERNS:
            matches = pattern.findall(content)
            assert len(matches) == 0, (
                f"skills/{skill_name}/SKILL.md: Hardcoded paths found: {matches}. "
                f"Use contextProvider/memoryStore interface references instead."
            )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_has_interface_references(self, skill_name):
        """SKILL.md must reference at least one interface (contextProvider or memoryStore)."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        has_interface = any(
            pattern.search(content)
            for pattern in INTERFACE_REFERENCE_PATTERNS
        )
        assert has_interface, (
            f"skills/{skill_name}/SKILL.md: No interface references found "
            f"(must reference contextProvider or memoryStore)"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_has_interface_references_section(self, skill_name):
        """SKILL.md must have an 'Interface References' section."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "Interface References" in content, (
            f"skills/{skill_name}/SKILL.md: Missing 'Interface References' section"
        )


# ---------------------------------------------------------------------------
# Mandatory Workflow Tests
# ---------------------------------------------------------------------------


class TestFrontendMobileWorkflow:
    """Validate mandatory workflow steps are present in SKILL.md."""

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_has_mandatory_workflow_section(self, skill_name):
        """SKILL.md must have a 'Mandatory Workflow' section."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "Mandatory Workflow" in content, (
            f"skills/{skill_name}/SKILL.md: Missing 'Mandatory Workflow' section"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    @pytest.mark.parametrize("keyword", MANDATORY_WORKFLOW_KEYWORDS)
    def test_has_mandatory_workflow_step(self, skill_name, keyword):
        """SKILL.md must include all mandatory workflow steps."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert keyword in content, (
            f"skills/{skill_name}/SKILL.md: Missing mandatory workflow step: '{keyword}'"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_has_compliance_checklist(self, skill_name):
        """SKILL.md must have a 'Compliance Checklist' section."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "Compliance Checklist" in content, (
            f"skills/{skill_name}/SKILL.md: Missing 'Compliance Checklist' section"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_has_version_history(self, skill_name):
        """SKILL.md must have a 'Version History' section."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "Version History" in content, (
            f"skills/{skill_name}/SKILL.md: Missing 'Version History' section"
        )


# ---------------------------------------------------------------------------
# Examples File Tests
# ---------------------------------------------------------------------------


class TestFrontendMobileExamples:
    """Validate examples.md files have sufficient content."""

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_examples_has_minimum_scenarios(self, skill_name):
        """examples.md must contain at least 3 example scenarios."""
        examples_md = SKILLS_DIR / skill_name / "examples.md"
        content = examples_md.read_text(encoding="utf-8")
        # Count ## Example N: patterns
        example_headers = re.findall(r"^## Example \d+", content, re.MULTILINE)
        assert len(example_headers) >= 3, (
            f"skills/{skill_name}/examples.md: Only {len(example_headers)} examples found, "
            f"need at least 3"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_examples_has_skill_invocation(self, skill_name):
        """examples.md must show skill invocation syntax."""
        examples_md = SKILLS_DIR / skill_name / "examples.md"
        content = examples_md.read_text(encoding="utf-8")
        assert f"skill:{skill_name}" in content, (
            f"skills/{skill_name}/examples.md: Missing 'skill:{skill_name}' invocation example"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_examples_has_expected_output(self, skill_name):
        """examples.md must describe expected output for scenarios."""
        examples_md = SKILLS_DIR / skill_name / "examples.md"
        content = examples_md.read_text(encoding="utf-8")
        assert "Expected Output" in content or "What Happens" in content, (
            f"skills/{skill_name}/examples.md: Missing 'Expected Output' or 'What Happens' section"
        )


# ---------------------------------------------------------------------------
# Memory Index Tests
# ---------------------------------------------------------------------------


class TestFrontendMobileMemory:
    """Validate memory index files exist and follow conventions."""

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_memory_directory_exists(self, skill_name):
        """Memory directory must exist for each skill."""
        mem_dir = MEMORY_DIR / skill_name
        assert mem_dir.is_dir(), (
            f"memory/skills/{skill_name}/ directory missing"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_memory_has_index(self, skill_name):
        """Memory directory must have index.md."""
        index_md = MEMORY_DIR / skill_name / "index.md"
        assert index_md.is_file(), (
            f"memory/skills/{skill_name}/index.md missing"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_memory_index_has_structure_section(self, skill_name):
        """Memory index must document the memory structure."""
        index_md = MEMORY_DIR / skill_name / "index.md"
        content = index_md.read_text(encoding="utf-8")
        assert "Memory Structure" in content, (
            f"memory/skills/{skill_name}/index.md: Missing 'Memory Structure' section"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_memory_index_has_version(self, skill_name):
        """Memory index must have Version field."""
        index_md = MEMORY_DIR / skill_name / "index.md"
        content = index_md.read_text(encoding="utf-8")
        assert "Version" in content, (
            f"memory/skills/{skill_name}/index.md: Missing 'Version' field"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_memory_index_has_last_updated(self, skill_name):
        """Memory index must have Last Updated field."""
        index_md = MEMORY_DIR / skill_name / "index.md"
        content = index_md.read_text(encoding="utf-8")
        assert "Last Updated" in content, (
            f"memory/skills/{skill_name}/index.md: Missing 'Last Updated' field"
        )

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_memory_index_references_skill(self, skill_name):
        """Memory index must reference its parent skill."""
        index_md = MEMORY_DIR / skill_name / "index.md"
        content = index_md.read_text(encoding="utf-8")
        assert skill_name in content, (
            f"memory/skills/{skill_name}/index.md: Doesn't reference skill '{skill_name}'"
        )


# ---------------------------------------------------------------------------
# Cross-Reference Tests
# ---------------------------------------------------------------------------


class TestFrontendMobileCrossReferences:
    """Validate cross-references between skill files and memory."""

    @pytest.mark.parametrize("skill_name", FRONTEND_MOBILE_SKILLS)
    def test_skill_memory_files_match_frontmatter(self, skill_name):
        """Memory files declared in frontmatter should be documented in memory index."""
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        fm = extract_yaml_frontmatter(skill_md)
        if fm is None:
            pytest.skip("No frontmatter")
        memory = fm.get("memory", {})
        scopes = memory.get("scopes", [])
        skill_scope = next((s for s in scopes if s.get("type") == "skill-specific"), None)
        if skill_scope is None:
            pytest.skip("No skill-specific scope")
        declared_files = skill_scope.get("files", [])
        index_md = MEMORY_DIR / skill_name / "index.md"
        if not index_md.exists():
            pytest.skip("No memory index")
        index_content = index_md.read_text(encoding="utf-8")
        for mem_file in declared_files:
            assert mem_file in index_content, (
                f"skills/{skill_name}: Memory file '{mem_file}' declared in frontmatter "
                f"but not documented in memory index"
            )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
