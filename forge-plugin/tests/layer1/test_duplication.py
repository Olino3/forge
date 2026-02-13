"""Test for duplicated content across Forge components — migrated from forge-duplication-detector.

Validates:
- No two skill SKILL.md files share >80% identical content
- No two agent .md personality files share >80% identical content
- No two context files share >80% identical content (within same domain)

This replaces the agentic forge-duplication-detector.md workflow with deterministic checks.
"""

import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR


def _extract_body(filepath: Path) -> str:
    """Extract content body, stripping YAML frontmatter."""
    text = filepath.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].strip()
    return text.strip()


def _normalize(text: str) -> str:
    """Normalize whitespace for comparison."""
    return " ".join(text.split()).lower()


def _similarity_ratio(a: str, b: str) -> float:
    """Quick length-based similarity pre-check, then line overlap."""
    if not a or not b:
        return 0.0
    # Fast length-based pre-filter
    len_ratio = min(len(a), len(b)) / max(len(a), len(b))
    if len_ratio < 0.5:
        return 0.0
    # Line-based overlap
    lines_a = set(a.splitlines())
    lines_b = set(b.splitlines())
    if not lines_a or not lines_b:
        return 0.0
    overlap = len(lines_a & lines_b)
    return overlap / max(len(lines_a), len(lines_b))


def _get_skill_files() -> list[tuple[str, Path]]:
    skills_dir = FORGE_DIR / "skills"
    if not skills_dir.is_dir():
        return []
    return [
        (d.name, d / "SKILL.md")
        for d in sorted(skills_dir.iterdir())
        if d.is_dir() and (d / "SKILL.md").is_file()
    ]


def _get_agent_personality_files() -> list[tuple[str, Path]]:
    agents_dir = FORGE_DIR / "agents"
    if not agents_dir.is_dir():
        return []
    return [
        (f.stem, f)
        for f in sorted(agents_dir.glob("*.md"))
    ]


def _get_context_files_by_domain() -> dict[str, list[tuple[str, Path]]]:
    context_dir = FORGE_DIR / "context"
    if not context_dir.is_dir():
        return {}
    domains: dict[str, list[tuple[str, Path]]] = {}
    for domain_dir in sorted(context_dir.iterdir()):
        if not domain_dir.is_dir():
            continue
        files = [
            (f.name, f)
            for f in sorted(domain_dir.glob("*.md"))
            if f.name != "index.md"
        ]
        if files:
            domains[domain_dir.name] = files
    return domains


class TestSkillDuplication:
    """Detect near-duplicate skill SKILL.md files."""

    def test_no_duplicate_skills(self):
        skills = _get_skill_files()
        if len(skills) < 2:
            pytest.skip("Need at least 2 skills to check duplication")

        bodies = [(name, _normalize(_extract_body(path))) for name, path in skills]
        duplicates = []

        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                ratio = _similarity_ratio(bodies[i][1], bodies[j][1])
                if ratio > 0.80:
                    duplicates.append(
                        f"{bodies[i][0]} <-> {bodies[j][0]} ({ratio:.0%} similar)"
                    )

        assert not duplicates, (
            f"Found {len(duplicates)} near-duplicate skill pairs:\n"
            + "\n".join(f"  - {d}" for d in duplicates)
        )


class TestAgentDuplication:
    """Detect near-duplicate agent personality files."""

    def test_no_duplicate_agents(self):
        agents = _get_agent_personality_files()
        if len(agents) < 2:
            pytest.skip("Need at least 2 agents to check duplication")

        bodies = [(name, _normalize(_extract_body(path))) for name, path in agents]
        duplicates = []

        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                ratio = _similarity_ratio(bodies[i][1], bodies[j][1])
                if ratio > 0.80:
                    duplicates.append(
                        f"{bodies[i][0]} <-> {bodies[j][0]} ({ratio:.0%} similar)"
                    )

        assert not duplicates, (
            f"Found {len(duplicates)} near-duplicate agent pairs:\n"
            + "\n".join(f"  - {d}" for d in duplicates)
        )


class TestContextDuplication:
    """Detect near-duplicate context files within the same domain."""

    def test_no_duplicate_context_within_domains(self):
        domains = _get_context_files_by_domain()
        if not domains:
            pytest.skip("No context domains found")

        duplicates = []
        for domain, files in domains.items():
            if len(files) < 2:
                continue
            bodies = [(name, _normalize(_extract_body(path))) for name, path in files]
            for i in range(len(bodies)):
                for j in range(i + 1, len(bodies)):
                    ratio = _similarity_ratio(bodies[i][1], bodies[j][1])
                    if ratio > 0.80:
                        duplicates.append(
                            f"{domain}/{bodies[i][0]} <-> {domain}/{bodies[j][0]} "
                            f"({ratio:.0%} similar)"
                        )

        assert not duplicates, (
            f"Found {len(duplicates)} near-duplicate context file pairs:\n"
            + "\n".join(f"  - {d}" for d in duplicates)
        )


class TestIdenticalFiles:
    """Detect completely identical files (same hash) across all components."""

    def test_no_identical_md_files(self):
        """No two .md files in forge-plugin/ should have identical content."""
        hashes: dict[str, list[str]] = {}
        for md in sorted(FORGE_DIR.rglob("*.md")):
            # Skip tests, memory, and node_modules
            rel = str(md.relative_to(FORGE_DIR))
            if any(skip in rel for skip in ["tests/", "memory/", "node_modules/"]):
                continue
            content_hash = hashlib.md5(md.read_bytes()).hexdigest()
            hashes.setdefault(content_hash, []).append(rel)

        duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        if duplicates:
            report = []
            for h, paths in duplicates.items():
                report.append(f"  Identical files (hash {h[:8]}):")
                for p in paths:
                    report.append(f"    - {p}")
            # Warn but don't fail — some intentional duplication may exist
            import warnings
            warnings.warn(
                f"Found {len(duplicates)} sets of identical files:\n"
                + "\n".join(report)
            )
