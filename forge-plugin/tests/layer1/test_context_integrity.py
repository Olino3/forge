"""Test context file integrity from forge-context-pruner workflow.

Validates:
1. Required frontmatter fields (id, domain, title, type, estimatedTokens, loadingStrategy, version, lastUpdated, sections, tags)
2. Index consistency - all files in domain are listed in index.md
3. Orphan detection - no files referenced in index that don't exist
4. Ghost detection - no files exist that aren't in index

Migrated from .github/workflows/forge-context-pruner.md as part of Phase 2 optimization.
"""

import re
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, extract_yaml_frontmatter


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_DOMAINS = {
    "engineering", "angular", "azure", "commands",
    "dotnet", "git", "python", "schema", "security",
}

REQUIRED_FRONTMATTER_FIELDS = {
    "id", "domain", "title", "type", "estimatedTokens",
    "loadingStrategy", "version", "lastUpdated", "sections", "tags"
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_context_files() -> list[tuple[str, Path]]:
    """Return (domain/filename, path) for all context .md files in domain subdirectories."""
    context_dir = FORGE_DIR / "context"
    files = []
    
    for domain_dir in sorted(context_dir.iterdir()):
        if domain_dir.is_dir() and domain_dir.name in VALID_DOMAINS:
            for md_file in sorted(domain_dir.rglob("*.md")):
                # Skip index files for the frontmatter test
                if md_file.name != "index.md":
                    rel_path = md_file.relative_to(context_dir)
                    files.append((str(rel_path), md_file))
    
    return files


def _get_domain_directories() -> list[tuple[str, Path]]:
    """Return (domain_name, domain_path) for all valid domain directories."""
    context_dir = FORGE_DIR / "context"
    return [
        (domain, context_dir / domain)
        for domain in sorted(VALID_DOMAINS)
        if (context_dir / domain).is_dir()
    ]


def _parse_index_references(index_path: Path) -> set[str]:
    """Extract all file references from domain index.md."""
    if not index_path.exists():
        return set()
    
    content = index_path.read_text(encoding='utf-8')
    # Match markdown links: [text](filename.md) or [text](subdir/filename.md)
    links = re.findall(r'\[.*?\]\(([^)]+\.md)\)', content)
    return {link for link in links if not link.startswith('http')}


# ---------------------------------------------------------------------------
# Test Classes
# ---------------------------------------------------------------------------

class TestContextFrontmatter:
    """Validate context file frontmatter compliance."""

    @pytest.mark.parametrize(
        "rel_path,file_path",
        _get_context_files(),
        ids=[rel_path for rel_path, _ in _get_context_files()],
    )
    def test_context_has_frontmatter(self, rel_path, file_path):
        """All context files must have YAML frontmatter."""
        frontmatter = extract_yaml_frontmatter(file_path)
        assert frontmatter is not None, (
            f"Context file '{rel_path}' missing YAML frontmatter"
        )

    @pytest.mark.parametrize(
        "rel_path,file_path",
        _get_context_files(),
        ids=[rel_path for rel_path, _ in _get_context_files()],
    )
    def test_context_required_fields(self, rel_path, file_path):
        """Check 1: Required frontmatter fields present."""
        frontmatter = extract_yaml_frontmatter(file_path)
        
        if frontmatter is None:
            pytest.skip(f"Context file '{rel_path}' has no frontmatter")
        
        missing_fields = REQUIRED_FRONTMATTER_FIELDS - set(frontmatter.keys())
        
        assert not missing_fields, (
            f"Context file '{rel_path}' missing required frontmatter fields:\n  " +
            "\n  ".join(sorted(missing_fields))
        )

    @pytest.mark.parametrize(
        "rel_path,file_path",
        _get_context_files(),
        ids=[rel_path for rel_path, _ in _get_context_files()],
    )
    def test_context_domain_consistency(self, rel_path, file_path):
        """Domain in frontmatter should match directory location."""
        frontmatter = extract_yaml_frontmatter(file_path)
        
        if frontmatter is None:
            pytest.skip(f"Context file '{rel_path}' has no frontmatter")
        
        frontmatter_domain = frontmatter.get('domain', '')
        # Extract domain from path (first directory after context/)
        path_domain = str(rel_path).split('/')[0]
        
        assert frontmatter_domain == path_domain, (
            f"Context file '{rel_path}' has domain '{frontmatter_domain}' in frontmatter "
            f"but is located in '{path_domain}' directory"
        )


class TestContextIndexIntegrity:
    """Validate context index consistency."""

    @pytest.mark.parametrize(
        "domain,domain_dir",
        _get_domain_directories(),
        ids=[domain for domain, _ in _get_domain_directories()],
    )
    def test_domain_has_index(self, domain, domain_dir):
        """Each domain directory must have an index.md."""
        index_path = domain_dir / "index.md"
        assert index_path.exists(), (
            f"Domain '{domain}' missing index.md"
        )

    @pytest.mark.parametrize(
        "domain,domain_dir",
        _get_domain_directories(),
        ids=[domain for domain, _ in _get_domain_directories()],
    )
    def test_no_orphaned_references(self, domain, domain_dir):
        """Check 3: No orphaned references - all files in index exist."""
        index_path = domain_dir / "index.md"
        
        if not index_path.exists():
            pytest.skip(f"Domain '{domain}' has no index.md")
        
        referenced_files = _parse_index_references(index_path)
        orphans = []
        
        for ref in referenced_files:
            ref_path = domain_dir / ref
            if not ref_path.exists():
                orphans.append(ref)
        
        assert not orphans, (
            f"Domain '{domain}' index.md references non-existent files:\n  " +
            "\n  ".join(orphans)
        )

    @pytest.mark.parametrize(
        "domain,domain_dir",
        _get_domain_directories(),
        ids=[domain for domain, _ in _get_domain_directories()],
    )
    def test_no_ghost_files(self, domain, domain_dir):
        """Check 4: No ghost files - all .md files (except index.md) are referenced in index."""
        index_path = domain_dir / "index.md"
        
        if not index_path.exists():
            pytest.skip(f"Domain '{domain}' has no index.md")
        
        referenced_files = _parse_index_references(index_path)
        existing_files = {
            str(f.relative_to(domain_dir))
            for f in domain_dir.rglob("*.md")
            if f.name != "index.md"
        }
        
        ghosts = existing_files - referenced_files
        
        assert not ghosts, (
            f"Domain '{domain}' has files not referenced in index.md (ghost files):\n  " +
            "\n  ".join(sorted(ghosts)) +
            "\n\nThese files should either be added to index.md or removed."
        )


class TestContextTopLevelIndex:
    """Validate top-level context/index.md."""

    def test_context_root_index_exists(self):
        """The context/ directory must have a root index.md."""
        root_index = FORGE_DIR / "context" / "index.md"
        assert root_index.exists(), (
            "Missing forge-plugin/context/index.md"
        )

    def test_context_root_index_lists_domains(self):
        """Root index should reference all domain subdirectories."""
        root_index = FORGE_DIR / "context" / "index.md"
        
        if not root_index.exists():
            pytest.skip("No root context/index.md")
        
        content = root_index.read_text(encoding='utf-8')
        
        # Check each valid domain is mentioned
        for domain in VALID_DOMAINS:
            domain_dir = FORGE_DIR / "context" / domain
            if domain_dir.is_dir():
                # Look for domain name or link to domain/index.md
                assert domain in content or f"{domain}/index.md" in content, (
                    f"Root context/index.md should reference domain '{domain}'"
                )
