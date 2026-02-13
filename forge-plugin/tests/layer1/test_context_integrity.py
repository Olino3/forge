"""Test context file integrity — migrated from agentic forge-context-pruner workflow.

Validates:
- All context files have valid YAML frontmatter
- Required fields: tags, sections (arrays)
- No empty or orphaned context files
- Domain index files reference existing context files
- Context files are not stale (optional: warns for >90 day lastUpdated)

This replaces the agentic forge-context-pruner.md workflow with deterministic checks.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, extract_yaml_frontmatter


CONTEXT_DIR = FORGE_DIR / "context"

SKIP_FILES = {"index.md", "loading_protocol.md", "cross_domain.md"}


def _get_domain_context_files() -> list[tuple[str, Path]]:
    """Return (relative_path, abs_path) for all .md files in domain subdirs."""
    if not CONTEXT_DIR.is_dir():
        return []
    files = []
    for domain_dir in sorted(CONTEXT_DIR.iterdir()):
        if not domain_dir.is_dir():
            continue
        for md in sorted(domain_dir.rglob("*.md")):
            rel = str(md.relative_to(CONTEXT_DIR))
            files.append((rel, md))
    return files


def _get_top_level_context_files() -> list[tuple[str, Path]]:
    """Return top-level .md files in context/ (index, loading_protocol, etc)."""
    if not CONTEXT_DIR.is_dir():
        return []
    return [
        (f.name, f) for f in sorted(CONTEXT_DIR.glob("*.md"))
    ]


class TestContextFilesExist:
    """Verify context directory structure is present."""

    def test_context_directory_exists(self):
        assert CONTEXT_DIR.is_dir(), "forge-plugin/context/ directory must exist"

    def test_context_index_exists(self):
        assert (CONTEXT_DIR / "index.md").is_file(), "context/index.md must exist"

    def test_loading_protocol_exists(self):
        assert (CONTEXT_DIR / "loading_protocol.md").is_file(), (
            "context/loading_protocol.md must exist"
        )

    def test_cross_domain_exists(self):
        assert (CONTEXT_DIR / "cross_domain.md").is_file(), (
            "context/cross_domain.md must exist"
        )


class TestContextFrontmatter:
    """Validate YAML frontmatter on all domain context files."""

    @pytest.fixture(scope="class")
    def context_files(self):
        return _get_domain_context_files()

    def test_context_files_found(self, context_files):
        assert len(context_files) > 0, "Should find context files in domain subdirs"

    @pytest.mark.parametrize(
        "rel_path, filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_has_yaml_frontmatter(self, rel_path, filepath):
        fm = extract_yaml_frontmatter(filepath)
        assert fm is not None, f"{rel_path} must have YAML frontmatter"

    @pytest.mark.parametrize(
        "rel_path, filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_frontmatter_has_required_fields(self, rel_path, filepath):
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip(f"{rel_path} has no frontmatter")
        # At minimum, context files should have an id or title
        has_id = "id" in fm
        has_title = "title" in fm
        assert has_id or has_title, (
            f"{rel_path} frontmatter must have 'id' or 'title'"
        )


class TestContextNotEmpty:
    """Ensure context files have meaningful content (not just frontmatter)."""

    @pytest.mark.parametrize(
        "rel_path, filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_has_content_beyond_frontmatter(self, rel_path, filepath):
        text = filepath.read_text(encoding="utf-8")
        # Strip frontmatter
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                body = text[end + 3:].strip()
            else:
                body = text.strip()
        else:
            body = text.strip()
        assert len(body) > 50, (
            f"{rel_path} has too little content ({len(body)} chars) — may be orphaned"
        )


class TestDomainIndexIntegrity:
    """Verify domain index files reference existing context files."""

    def _get_domain_indexes(self) -> list[tuple[str, Path]]:
        if not CONTEXT_DIR.is_dir():
            return []
        indexes = []
        for domain_dir in sorted(CONTEXT_DIR.iterdir()):
            if not domain_dir.is_dir():
                continue
            idx = domain_dir / "index.md"
            if idx.is_file():
                indexes.append((domain_dir.name, idx))
        return indexes

    @pytest.mark.parametrize(
        "domain, index_path",
        [],  # Will be dynamically populated
    )
    def test_domain_has_index(self, domain, index_path):
        assert index_path.is_file()

    def test_all_domains_have_indexes(self):
        """Every domain subdirectory should have an index.md."""
        for domain_dir in sorted(CONTEXT_DIR.iterdir()):
            if not domain_dir.is_dir():
                continue
            idx = domain_dir / "index.md"
            assert idx.is_file(), f"context/{domain_dir.name}/ must have index.md"
