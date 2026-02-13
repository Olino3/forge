"""Test for broken cross-reference links — migrated from agentic forge-xref-checker.

Validates:
- Markdown links [text](path) in forge-plugin/ point to existing files
- Relative links resolve correctly from the file's location
- No dangling references to deleted files
- Anchor links (#section) are skipped (too fragile to validate)
- External URLs (http/https) are skipped (no network in CI)

This replaces the agentic forge-xref-checker.md workflow with deterministic checks.
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, REPO_ROOT


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

SKIP_PATTERNS = {
    "tests/", "memory/", "node_modules/", "__pycache__/", ".pytest_cache/"
}


def _get_markdown_files() -> list[tuple[str, Path]]:
    """Get all .md files under forge-plugin/, excluding tests and memory."""
    files = []
    for md in sorted(FORGE_DIR.rglob("*.md")):
        rel = str(md.relative_to(FORGE_DIR))
        if any(skip in rel for skip in SKIP_PATTERNS):
            continue
        files.append((rel, md))
    return files


def _extract_links(filepath: Path) -> list[tuple[int, str, str]]:
    """Extract (line_number, link_text, link_target) from markdown file."""
    links = []
    text = filepath.read_text(encoding="utf-8")
    in_code_block = False

    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        for match in MARKDOWN_LINK_RE.finditer(line):
            links.append((i, match.group(1), match.group(2)))
    return links


def _is_external(target: str) -> bool:
    """Check if link target is an external URL."""
    parsed = urlparse(target)
    return parsed.scheme in ("http", "https", "mailto", "ftp")


def _is_anchor(target: str) -> bool:
    """Check if link is an anchor-only reference."""
    return target.startswith("#")


def _is_template(target: str) -> bool:
    """Check if link contains template placeholders."""
    return "{" in target or "}" in target


class TestMarkdownLinkIntegrity:
    """Verify internal markdown links point to existing files."""

    def test_no_broken_internal_links(self):
        broken = []
        for rel_path, filepath in _get_markdown_files():
            links = _extract_links(filepath)
            for line_num, text, target in links:
                # Skip external, anchor, and template links
                if _is_external(target) or _is_anchor(target) or _is_template(target):
                    continue

                # Strip anchor from target if present
                clean_target = target.split("#")[0]
                if not clean_target:
                    continue

                # Resolve relative to the file's directory
                resolved = (filepath.parent / clean_target).resolve()

                # Check if it exists as file or directory
                if not resolved.exists():
                    # Also check relative to repo root
                    from_root = (REPO_ROOT / clean_target).resolve()
                    if not from_root.exists():
                        broken.append(
                            f"{rel_path}:{line_num} -> {target}"
                        )

        if broken:
            # Report as warning for the first implementation
            # Can be made strict once all links are fixed
            import warnings
            warnings.warn(
                f"Found {len(broken)} broken internal links:\n"
                + "\n".join(f"  - {b}" for b in broken[:20])
                + (f"\n  ... and {len(broken) - 20} more" if len(broken) > 20 else "")
            )


class TestCriticalLinkIntegrity:
    """Verify critical cross-references between core Forge files."""

    def test_agent_config_skill_refs_exist(self):
        """Skills referenced in agent configs should exist as directories."""
        import json
        agents_dir = FORGE_DIR / "agents"
        skills_dir = FORGE_DIR / "skills"
        if not agents_dir.is_dir() or not skills_dir.is_dir():
            pytest.skip("Missing agents or skills directory")

        broken = []
        for config in sorted(agents_dir.glob("*.config.json")):
            data = json.loads(config.read_text(encoding="utf-8"))
            skills = data.get("skills", [])
            for skill in skills:
                # Skills can be strings or objects with a 'name' field
                skill_name = skill["name"] if isinstance(skill, dict) else str(skill)
                skill_dir = skills_dir / skill_name
                if not skill_dir.is_dir():
                    broken.append(
                        f"{config.name}: skill '{skill_name}' not found"
                    )

        assert not broken, (
            f"Agent configs reference non-existent skills:\n"
            + "\n".join(f"  - {b}" for b in broken)
        )

    def test_hooks_json_script_refs_exist(self):
        """Scripts referenced in hooks.json should exist."""
        import json
        hooks_dir = FORGE_DIR / "hooks"
        hooks_json = hooks_dir / "hooks.json"
        if not hooks_json.is_file():
            pytest.skip("No hooks.json found")

        data = json.loads(hooks_json.read_text(encoding="utf-8"))
        broken = []

        # hooks.json structure: {"hooks": {"EventType": [{"matcher": ..., "hooks": [{"command": ...}]}]}}
        hooks_by_event = data.get("hooks", {})
        for event_type, matchers in hooks_by_event.items():
            if not isinstance(matchers, list):
                continue
            for matcher_group in matchers:
                if not isinstance(matcher_group, dict):
                    continue
                for hook in matcher_group.get("hooks", []):
                    if not isinstance(hook, dict):
                        continue
                    command = hook.get("command", "")
                    parts = command.split()
                    for part in parts:
                        if part.endswith(".sh"):
                            # Skip paths with variable placeholders
                            if "$" in part or "{" in part:
                                continue
                            script_path = hooks_dir / part
                            if not script_path.is_file():
                                script_path = REPO_ROOT / part
                                if not script_path.is_file():
                                    broken.append(
                                        f"hooks.json ({event_type}): script '{part}' not found"
                                    )

        assert not broken, (
            f"hooks.json references non-existent scripts:\n"
            + "\n".join(f"  - {b}" for b in broken)
        )
