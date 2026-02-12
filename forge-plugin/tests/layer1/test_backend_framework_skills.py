"""Validate Backend & Frameworks skill definitions."""

import pytest

from conftest import FORGE_DIR, extract_yaml_frontmatter


BACKEND_SKILLS = (
    "django",
    "dotnet-core",
    "fastapi",
    "nestjs",
    "rails",
    "php",
)


class TestBackendFrameworkSkills:
    """Ensure backend framework skills have required structure and metadata."""

    @pytest.mark.parametrize("skill_name", BACKEND_SKILLS)
    def test_skill_files_and_memory_index(self, skill_name):
        skill_dir = FORGE_DIR / "skills" / skill_name
        assert skill_dir.is_dir(), f"Missing skills/{skill_name}/ directory"
        assert (skill_dir / "SKILL.md").is_file(), (
            f"skills/{skill_name}/SKILL.md missing"
        )
        assert (skill_dir / "examples.md").is_file(), (
            f"skills/{skill_name}/examples.md missing"
        )
        memory_index = (
            FORGE_DIR / "memory" / "skills" / skill_name / "index.md"
        )
        assert memory_index.is_file(), (
            f"memory/skills/{skill_name}/index.md missing"
        )

    @pytest.mark.parametrize("skill_name", BACKEND_SKILLS)
    def test_skill_frontmatter_required_fields(self, skill_name):
        skill_md = FORGE_DIR / "skills" / skill_name / "SKILL.md"
        frontmatter = extract_yaml_frontmatter(skill_md)
        assert frontmatter, f"Missing YAML frontmatter in {skill_md}"
        assert frontmatter.get("name") == skill_name
        for field in ("version", "description", "context", "memory", "tags"):
            assert field in frontmatter, (
                f"{skill_name} frontmatter missing '{field}'"
            )
