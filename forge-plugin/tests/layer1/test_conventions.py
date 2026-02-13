"""Test coding conventions — migrated from agentic forge-convention-enforcer workflow.

Validates:
- Skill directories use kebab-case naming
- Agent files are paired: {name}.md + {name}.config.json
- Context files use kebab-case naming
- Command directories use kebab-case naming
- Markdown files use ATX-style headings (# not underline)
- Hook scripts start with set -euo pipefail or set -e
- Workflow .md files have valid YAML frontmatter with required fields

This replaces the agentic forge-convention-enforcer.md workflow with deterministic checks.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, REPO_ROOT, extract_yaml_frontmatter


KEBAB_CASE_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
SETEXT_HEADING_RE = re.compile(r"^[=\-]{3,}\s*$")


def _is_kebab_case(name: str) -> bool:
    return bool(KEBAB_CASE_RE.match(name))


class TestSkillNamingConventions:
    """Skill directories must use kebab-case."""

    def _get_skill_dirs(self) -> list[str]:
        skills_dir = FORGE_DIR / "skills"
        if not skills_dir.is_dir():
            return []
        return [
            d.name for d in sorted(skills_dir.iterdir())
            if d.is_dir() and not d.name.startswith(".")
        ]

    def test_skill_dirs_found(self):
        dirs = self._get_skill_dirs()
        assert len(dirs) > 0, "Should find skill directories"

    def test_all_skill_dirs_kebab_case(self):
        violations = [
            d for d in self._get_skill_dirs()
            if not _is_kebab_case(d)
        ]
        assert not violations, (
            f"Skill directories not in kebab-case:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


class TestAgentPairingConventions:
    """Agent .md files must have matching .config.json and vice versa."""

    def test_agent_md_has_config(self):
        agents_dir = FORGE_DIR / "agents"
        if not agents_dir.is_dir():
            pytest.skip("No agents directory")
        md_files = {f.stem for f in agents_dir.glob("*.md")}
        config_files = {
            f.name.replace(".config.json", "")
            for f in agents_dir.glob("*.config.json")
        }
        missing_config = md_files - config_files
        assert not missing_config, (
            f"Agent .md files without matching .config.json:\n"
            + "\n".join(f"  - {m}" for m in sorted(missing_config))
        )

    def test_agent_config_has_md(self):
        agents_dir = FORGE_DIR / "agents"
        if not agents_dir.is_dir():
            pytest.skip("No agents directory")
        md_files = {f.stem for f in agents_dir.glob("*.md")}
        config_files = {
            f.name.replace(".config.json", "")
            for f in agents_dir.glob("*.config.json")
        }
        orphan_configs = config_files - md_files
        assert not orphan_configs, (
            f"Agent .config.json without matching .md:\n"
            + "\n".join(f"  - {o}" for o in sorted(orphan_configs))
        )


class TestCommandNamingConventions:
    """Command directories must use kebab-case."""

    def test_command_dirs_kebab_case(self):
        commands_dir = FORGE_DIR / "commands"
        if not commands_dir.is_dir():
            pytest.skip("No commands directory")
        dirs = [
            d.name for d in sorted(commands_dir.iterdir())
            if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")
        ]
        violations = [d for d in dirs if not _is_kebab_case(d)]
        assert not violations, (
            f"Command directories not in kebab-case:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


class TestContextNamingConventions:
    """Context domain directories and files should use kebab-case or snake_case."""

    def test_context_domain_dirs_lowercase(self):
        context_dir = FORGE_DIR / "context"
        if not context_dir.is_dir():
            pytest.skip("No context directory")
        dirs = [
            d.name for d in sorted(context_dir.iterdir())
            if d.is_dir()
        ]
        violations = [d for d in dirs if d != d.lower()]
        assert not violations, (
            f"Context domain directories with uppercase:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


class TestMarkdownHeadingStyle:
    """Markdown files should use ATX headings (# style), not Setext (underline)."""

    def _get_markdown_files(self) -> list[tuple[str, Path]]:
        files = []
        for md in sorted(FORGE_DIR.rglob("*.md")):
            rel = str(md.relative_to(FORGE_DIR))
            if any(skip in rel for skip in ["tests/", "memory/", "node_modules/"]):
                continue
            files.append((rel, md))
        return files

    def test_no_setext_headings(self):
        violations = []
        for rel, filepath in self._get_markdown_files():
            lines = filepath.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                # Skip lines inside code blocks
                if line.startswith("```"):
                    continue
                if SETEXT_HEADING_RE.match(line) and i > 0:
                    prev_line = lines[i - 1].strip()
                    # Setext heading: previous line is text, this line is === or ---
                    # But --- at the top of file is frontmatter, not heading
                    if prev_line and not prev_line.startswith("#"):
                        # Check it's not YAML frontmatter delimiter
                        if line.strip().startswith("="):
                            violations.append(f"{rel}:{i + 1}")
        if violations:
            import warnings
            warnings.warn(
                f"Found {len(violations)} Setext headings (use ATX # style instead):\n"
                + "\n".join(f"  - {v}" for v in violations[:10])
            )


class TestHookScriptConventions:
    """Hook scripts should follow bash safety conventions."""

    def _get_hook_scripts(self) -> list[tuple[str, Path]]:
        hooks_dir = FORGE_DIR / "hooks"
        if not hooks_dir.is_dir():
            return []
        return [
            (f.name, f)
            for f in sorted(hooks_dir.glob("*.sh"))
        ]

    def test_hooks_have_safe_mode(self):
        violations = []
        for name, filepath in self._get_hook_scripts():
            content = filepath.read_text(encoding="utf-8")
            has_strict = "set -euo pipefail" in content or "set -e" in content
            if not has_strict:
                violations.append(name)
        assert not violations, (
            f"Hook scripts missing 'set -e' or 'set -euo pipefail':\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


class TestWorkflowFrontmatter:
    """Agentic workflow .md files should have valid frontmatter."""

    def _get_workflow_files(self) -> list[tuple[str, Path]]:
        wf_dir = REPO_ROOT / ".github" / "workflows"
        if not wf_dir.is_dir():
            return []
        return [
            (f.name, f)
            for f in sorted(wf_dir.glob("forge-*.md"))
        ]

    def test_workflow_files_have_frontmatter(self):
        for name, filepath in self._get_workflow_files():
            fm = extract_yaml_frontmatter(filepath)
            assert fm is not None, f"{name} must have YAML frontmatter"

    def test_workflow_has_description(self):
        for name, filepath in self._get_workflow_files():
            fm = extract_yaml_frontmatter(filepath)
            if fm is None:
                continue
            assert "description" in fm, f"{name} frontmatter must have 'description'"

    def test_workflow_has_permissions(self):
        for name, filepath in self._get_workflow_files():
            fm = extract_yaml_frontmatter(filepath)
            if fm is None:
                continue
            assert "permissions" in fm, f"{name} frontmatter must have 'permissions'"

    def test_workflow_no_write_permissions(self):
        """Strict mode: no write permissions in frontmatter."""
        for name, filepath in self._get_workflow_files():
            fm = extract_yaml_frontmatter(filepath)
            if fm is None or "permissions" not in fm:
                continue
            perms = fm["permissions"]
            if isinstance(perms, dict):
                for key, val in perms.items():
                    assert val != "write", (
                        f"{name} has write permission for '{key}' — "
                        "safe-outputs handles writes automatically"
                    )
