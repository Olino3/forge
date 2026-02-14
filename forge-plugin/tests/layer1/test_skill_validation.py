"""Test skill structure validation from forge-skill-validator workflow.

Validates:
1. Template compliance - SKILL.md contains required template sections
2. 6-step workflow compliance (Initial Analysis, Load Memory, Load Context, Perform Analysis, Generate Output, Update Memory)
3. Examples presence - Directory includes examples.md
4. Skill isolation - No hardcoded references to other skills or filesystem paths
5. Output conventions - References OUTPUT_CONVENTIONS.md where appropriate

Migrated from .github/workflows/forge-skill-validator.md as part of Phase 2 optimization.
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

# Required sections from SKILL_TEMPLATE.md
REQUIRED_SECTIONS = [
    "## Purpose",
    "## Prerequisites",
    "## Workflow",
    "## Input Format",
    "## Output Format",
    "## Examples",
]

# 6-step workflow keywords (must appear in workflow section)
SIX_STEP_KEYWORDS = [
    r"Initial\s+Analysis",
    r"Load\s+Memory",
    r"Load\s+Context",
    r"Perform\s+Analysis",
    r"Generate\s+Output",
    r"Update\s+Memory",
]

# Patterns that indicate hardcoded paths (bad practice)
HARDCODED_PATH_PATTERNS = [
    r'forge-plugin/skills/[a-z-]+',
    r'\./skills/',
    r'\.\./skills/',
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_skill_directories() -> list[tuple[str, Path]]:
    """Return (skill_name, skill_dir) for all skill directories."""
    skills_dir = FORGE_DIR / "skills"
    # Filter out non-directory items and template
    skill_dirs = [
        d for d in sorted(skills_dir.iterdir())
        if d.is_dir() and d.name not in ["SKILL_TEMPLATE.md", "__pycache__"]
    ]
    return [(d.name, d) for d in skill_dirs]


def _read_skill_md(skill_dir: Path) -> str:
    """Read SKILL.md content or return empty string if not found."""
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        return skill_md.read_text(encoding='utf-8')
    return ""


# ---------------------------------------------------------------------------
# Test Class
# ---------------------------------------------------------------------------

class TestSkillValidation:
    """Validate skill structure per forge-skill-validator.md checks."""

    @pytest.mark.parametrize(
        "skill_name,skill_dir",
        _get_skill_directories(),
        ids=[name for name, _ in _get_skill_directories()],
    )
    def test_skill_has_skill_md(self, skill_name, skill_dir):
        """All skill directories must have SKILL.md."""
        skill_md = skill_dir / "SKILL.md"
        assert skill_md.exists(), (
            f"Skill '{skill_name}' missing SKILL.md file"
        )

    @pytest.mark.parametrize(
        "skill_name,skill_dir",
        _get_skill_directories(),
        ids=[name for name, _ in _get_skill_directories()],
    )
    def test_skill_template_compliance(self, skill_name, skill_dir):
        """Check 1: SKILL.md contains required template sections."""
        content = _read_skill_md(skill_dir)
        
        if not content:
            pytest.skip(f"Skill '{skill_name}' has no SKILL.md")
        
        missing_sections = []
        for section in REQUIRED_SECTIONS:
            if section not in content:
                missing_sections.append(section)
        
        assert not missing_sections, (
            f"Skill '{skill_name}' missing required sections:\n  " +
            "\n  ".join(missing_sections)
        )

    @pytest.mark.parametrize(
        "skill_name,skill_dir",
        _get_skill_directories(),
        ids=[name for name, _ in _get_skill_directories()],
    )
    def test_skill_six_step_workflow(self, skill_name, skill_dir):
        """Check 2: Skill follows 6-step workflow."""
        content = _read_skill_md(skill_dir)
        
        if not content:
            pytest.skip(f"Skill '{skill_name}' has no SKILL.md")
        
        missing_steps = []
        for step_pattern in SIX_STEP_KEYWORDS:
            if not re.search(step_pattern, content, re.IGNORECASE):
                missing_steps.append(step_pattern.replace(r'\s+', ' '))
        
        assert not missing_steps, (
            f"Skill '{skill_name}' missing 6-step workflow elements:\n  " +
            "\n  ".join(missing_steps) +
            "\n\nExpected all 6 steps: Initial Analysis, Load Memory, Load Context, " +
            "Perform Analysis, Generate Output, Update Memory"
        )

    @pytest.mark.parametrize(
        "skill_name,skill_dir",
        _get_skill_directories(),
        ids=[name for name, _ in _get_skill_directories()],
    )
    def test_skill_has_examples(self, skill_name, skill_dir):
        """Check 3: Directory includes examples.md."""
        examples_md = skill_dir / "examples.md"
        assert examples_md.exists(), (
            f"Skill '{skill_name}' missing examples.md file"
        )

    @pytest.mark.parametrize(
        "skill_name,skill_dir",
        _get_skill_directories(),
        ids=[name for name, _ in _get_skill_directories()],
    )
    def test_skill_isolation(self, skill_name, skill_dir):
        """Check 4: No hardcoded references to other skills or filesystem paths."""
        content = _read_skill_md(skill_dir)
        
        if not content:
            pytest.skip(f"Skill '{skill_name}' has no SKILL.md")
        
        violations = []
        for pattern in HARDCODED_PATH_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                violations.extend(matches)
        
        assert not violations, (
            f"Skill '{skill_name}' contains hardcoded paths (violates skill isolation):\n  " +
            "\n  ".join(set(violations)) +
            "\n\nUse interface references instead (e.g., contextProvider.load(), skillInvoker.invoke())"
        )

    @pytest.mark.parametrize(
        "skill_name,skill_dir",
        _get_skill_directories(),
        ids=[name for name, _ in _get_skill_directories()],
    )
    def test_skill_output_conventions_reference(self, skill_name, skill_dir):
        """Check 5: References OUTPUT_CONVENTIONS.md where output format is defined."""
        content = _read_skill_md(skill_dir)
        
        if not content:
            pytest.skip(f"Skill '{skill_name}' has no SKILL.md")
        
        # Check if skill defines output format
        has_output_section = "## Output Format" in content
        references_conventions = "OUTPUT_CONVENTIONS" in content or "output_conventions" in content.lower()
        
        if has_output_section and "/claudedocs/" in content:
            # If skill outputs to /claudedocs/, it should reference OUTPUT_CONVENTIONS
            assert references_conventions, (
                f"Skill '{skill_name}' outputs to /claudedocs/ but doesn't reference OUTPUT_CONVENTIONS.md. "
                f"Add reference to ensure consistent output formatting."
            )
