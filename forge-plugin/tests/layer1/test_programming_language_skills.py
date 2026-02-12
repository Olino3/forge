"""Validate Programming Languages skills content and structure."""

from pathlib import Path

import pytest

from conftest import FORGE_DIR, extract_yaml_frontmatter


SKILL_METADATA = {
    "cpp": {
        "description": "Modern C++ (C++17/20/23) development and best practices",
        "primary_domain": "engineering",
        "memory_files": {
            "project_overview.md",
            "toolchain_profile.md",
            "performance_notes.md",
            "known_issues.md",
        },
    },
    "csharp": {
        "description": "C# language features and .NET ecosystem development",
        "primary_domain": "dotnet",
        "memory_files": {
            "project_overview.md",
            "runtime_stack.md",
            "csharp_conventions.md",
            "known_issues.md",
        },
    },
    "java-architect": {
        "description": "Enterprise Java architecture and design patterns",
        "primary_domain": "engineering",
        "memory_files": {
            "project_overview.md",
            "architecture_decisions.md",
            "framework_stack.md",
            "performance_notes.md",
        },
    },
    "javascript": {
        "description": "Advanced JavaScript patterns, ES2024+, and runtime optimization",
        "primary_domain": "engineering",
        "memory_files": {
            "project_overview.md",
            "runtime_profile.md",
            "module_strategy.md",
            "performance_notes.md",
        },
    },
    "typescript": {
        "description": "TypeScript advanced types, generics, and strict configuration",
        "primary_domain": "engineering",
        "memory_files": {
            "project_overview.md",
            "tsconfig_profile.md",
            "type_patterns.md",
            "migration_notes.md",
        },
    },
}

WORKFLOW_STEPS = [
    "Initial Analysis",
    "Load Memory",
    "Load Context",
    "Perform Analysis",
    "Generate Output",
    "Update Memory",
]


def _skill_path(skill: str) -> Path:
    return FORGE_DIR / "skills" / skill / "SKILL.md"


def _examples_path(skill: str) -> Path:
    return FORGE_DIR / "skills" / skill / "examples.md"


def _memory_index_path(skill: str) -> Path:
    return FORGE_DIR / "memory" / "skills" / skill / "index.md"


@pytest.mark.parametrize("skill", SKILL_METADATA.keys())
def test_skill_frontmatter(skill):
    skill_path = _skill_path(skill)
    assert skill_path.exists(), f"Missing SKILL.md for {skill}"

    frontmatter = extract_yaml_frontmatter(skill_path)
    assert frontmatter is not None, f"Missing frontmatter for {skill}"

    expected = SKILL_METADATA[skill]
    for key in ["name", "version", "description", "context", "memory", "tags"]:
        assert key in frontmatter, f"{skill} missing frontmatter field: {key}"

    assert frontmatter["name"] == skill
    assert frontmatter["version"] == "1.0.0"
    assert frontmatter["description"] == expected["description"]
    assert frontmatter["context"]["primary_domain"] == expected["primary_domain"]

    scopes = frontmatter["memory"].get("scopes", [])
    skill_scope = next(
        (scope for scope in scopes if scope.get("type") == "skill-specific"),
        None,
    )
    assert skill_scope is not None, f"{skill} missing skill-specific memory scope"
    assert set(skill_scope.get("files", [])) == expected["memory_files"]


@pytest.mark.parametrize("skill", SKILL_METADATA.keys())
def test_skill_content_has_interfaces_and_output(skill):
    content = _skill_path(skill).read_text(encoding="utf-8")
    assert "contextProvider" in content
    assert "memoryStore" in content
    assert "/claudedocs/" in content
    assert "OUTPUT_CONVENTIONS" in content


@pytest.mark.parametrize("skill", SKILL_METADATA.keys())
def test_skill_has_mandatory_workflow_steps(skill):
    content = _skill_path(skill).read_text(encoding="utf-8").lower()
    for step in WORKFLOW_STEPS:
        assert step.lower() in content, f"{skill} missing workflow step: {step}"


@pytest.mark.parametrize("skill", SKILL_METADATA.keys())
def test_examples_have_three_scenarios(skill):
    examples = _examples_path(skill).read_text(encoding="utf-8")
    assert examples.count("## Example") >= 3


@pytest.mark.parametrize("skill", SKILL_METADATA.keys())
def test_memory_index_exists(skill):
    memory_index = _memory_index_path(skill)
    assert memory_index.exists(), f"Missing memory index for {skill}"
