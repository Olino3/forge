"""Tests for context loading protocol — independent of hooks.

Validates the 5-step context loading protocol from loading_protocol.md:
  1. Every domain has an index.md
  2. Index files with indexedFiles reference existing files
  3. loadingStrategy: always files have appropriate type
  4. estimatedTokens values are reasonable (> 0, < 10000)
  5. Domain consistency (file's domain field matches parent dir name)

These tests validate the *specification* rather than hook behaviour,
checking that all context files conform to the protocol requirements.
"""

from pathlib import Path

import pytest
import yaml

from conftest import FORGE_DIR, extract_yaml_frontmatter


CONTEXT_DIR = FORGE_DIR / "context"

# Known domains from the Forge spec
KNOWN_DOMAINS = [
    "angular",
    "azure",
    "commands",
    "dotnet",
    "engineering",
    "git",
    "python",
    "schema",
    "security",
]

# Top-level special files that are not domain directories
SPECIAL_FILES = {"cross_domain.md", "loading_protocol.md", "index.md"}

# Files exempt from frontmatter requirements (special structure)
FRONTMATTER_EXEMPT = {"cross_domain.md", "loading_protocol.md"}


def _get_domain_dirs() -> list[Path]:
    """Return all domain subdirectories in context/."""
    return [
        d
        for d in CONTEXT_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]


def _get_context_files_with_frontmatter() -> list[tuple[Path, dict]]:
    """Return (path, frontmatter) for all context .md files with valid frontmatter."""
    results = []
    for domain_dir in _get_domain_dirs():
        for md_file in domain_dir.glob("*.md"):
            fm = extract_yaml_frontmatter(md_file)
            if fm:
                results.append((md_file, fm))
    return results


# ── Step 1: Every domain has index.md ────────────────────────────────

class TestDomainIndexes:
    """Every domain directory must have an index.md."""

    @pytest.mark.parametrize("domain", KNOWN_DOMAINS)
    def test_domain_has_index(self, domain):
        """Domain '{domain}' should have an index.md file."""
        index_path = CONTEXT_DIR / domain / "index.md"
        assert index_path.exists(), (
            f"Domain '{domain}' is missing index.md at {index_path}"
        )

    @pytest.mark.parametrize("domain", KNOWN_DOMAINS)
    def test_domain_index_has_frontmatter(self, domain):
        """Domain index.md should have valid YAML frontmatter."""
        index_path = CONTEXT_DIR / domain / "index.md"
        if not index_path.exists():
            pytest.skip(f"Index not found for {domain}")
        fm = extract_yaml_frontmatter(index_path)
        assert fm is not None, f"index.md for '{domain}' has no valid frontmatter"

    @pytest.mark.parametrize("domain", KNOWN_DOMAINS)
    def test_domain_index_type_is_index(self, domain):
        """Domain index.md should have type 'index'."""
        index_path = CONTEXT_DIR / domain / "index.md"
        if not index_path.exists():
            pytest.skip(f"Index not found for {domain}")
        fm = extract_yaml_frontmatter(index_path)
        if fm is None:
            pytest.skip(f"No frontmatter in {domain}/index.md")
        assert fm.get("type") == "index", (
            f"{domain}/index.md has type '{fm.get('type')}' instead of 'index'"
        )


# ── Step 2: Index indexedFiles reference existing files ──────────────

class TestIndexedFileReferences:
    """Index files with indexedFiles entries must reference existing files."""

    @pytest.mark.parametrize("domain", KNOWN_DOMAINS)
    def test_indexed_files_exist(self, domain):
        """All indexedFiles paths in {domain}/index.md should exist."""
        index_path = CONTEXT_DIR / domain / "index.md"
        if not index_path.exists():
            pytest.skip(f"Index not found for {domain}")
        fm = extract_yaml_frontmatter(index_path)
        if fm is None:
            pytest.skip(f"No frontmatter in {domain}/index.md")

        indexed_files = fm.get("indexedFiles", [])
        if not indexed_files:
            pytest.skip(f"No indexedFiles in {domain}/index.md")

        missing = []
        for entry in indexed_files:
            rel_path = entry.get("path", "")
            if not rel_path:
                continue
            full_path = CONTEXT_DIR / domain / rel_path
            if not full_path.exists():
                missing.append(rel_path)

        assert not missing, (
            f"{domain}/index.md references non-existent files: {missing}"
        )

    @pytest.mark.parametrize("domain", KNOWN_DOMAINS)
    def test_indexed_files_have_ids(self, domain):
        """All indexedFiles entries should have an 'id' field."""
        index_path = CONTEXT_DIR / domain / "index.md"
        if not index_path.exists():
            pytest.skip(f"Index not found for {domain}")
        fm = extract_yaml_frontmatter(index_path)
        if fm is None:
            pytest.skip(f"No frontmatter in {domain}/index.md")

        indexed_files = fm.get("indexedFiles", [])
        if not indexed_files:
            pytest.skip(f"No indexedFiles in {domain}/index.md")

        for entry in indexed_files:
            assert "id" in entry, (
                f"{domain}/index.md has indexedFile entry without 'id': {entry}"
            )


# ── Step 3: loadingStrategy always files ─────────────────────────────

class TestAlwaysLoadFiles:
    """Files with loadingStrategy 'always' should have appropriate types."""

    VALID_ALWAYS_TYPES = {"always", "index", "detection", "reference"}

    def test_always_load_files_have_valid_types(self):
        """All files with loadingStrategy=always must have valid types."""
        invalid = []
        for path, fm in _get_context_files_with_frontmatter():
            if fm.get("loadingStrategy") == "always":
                file_type = fm.get("type", "")
                if file_type not in self.VALID_ALWAYS_TYPES:
                    invalid.append(
                        f"{path.relative_to(FORGE_DIR)}: type={file_type}"
                    )
        assert not invalid, (
            f"Files with loadingStrategy=always have invalid types:\n"
            + "\n".join(f"  - {f}" for f in invalid)
        )


# ── Step 4: estimatedTokens validation ──────────────────────────────

class TestEstimatedTokens:
    """estimatedTokens should be reasonable: > 0 and < 10000."""

    def test_all_estimated_tokens_positive(self):
        """estimatedTokens must be a positive integer."""
        violations = []
        for path, fm in _get_context_files_with_frontmatter():
            tokens = fm.get("estimatedTokens")
            if tokens is not None:
                if not isinstance(tokens, int) or tokens < 1:
                    violations.append(
                        f"{path.relative_to(FORGE_DIR)}: estimatedTokens={tokens}"
                    )
        assert not violations, (
            f"Files with invalid estimatedTokens:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_all_estimated_tokens_under_10000(self):
        """estimatedTokens should be < 10000 (no single file that large)."""
        violations = []
        for path, fm in _get_context_files_with_frontmatter():
            tokens = fm.get("estimatedTokens")
            if tokens is not None and isinstance(tokens, int) and tokens >= 10000:
                violations.append(
                    f"{path.relative_to(FORGE_DIR)}: estimatedTokens={tokens}"
                )
        assert not violations, (
            f"Files with unreasonably large estimatedTokens:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_section_tokens_positive(self):
        """Section-level estimatedTokens should also be positive."""
        violations = []
        for path, fm in _get_context_files_with_frontmatter():
            sections = fm.get("sections", [])
            for section in sections:
                tokens = section.get("estimatedTokens")
                if tokens is not None:
                    if not isinstance(tokens, int) or tokens < 1:
                        violations.append(
                            f"{path.relative_to(FORGE_DIR)} section "
                            f"'{section.get('name', '?')}': "
                            f"estimatedTokens={tokens}"
                        )
        assert not violations, (
            f"Sections with invalid estimatedTokens:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


# ── Step 5: Domain consistency ───────────────────────────────────────

class TestDomainConsistency:
    """File's domain field must match its parent directory name."""

    def test_domain_matches_parent_dir(self):
        """Every context file's 'domain' field should match its directory name."""
        mismatches = []
        for path, fm in _get_context_files_with_frontmatter():
            file_domain = fm.get("domain", "")
            parent_dir = path.parent.name
            if file_domain != parent_dir:
                mismatches.append(
                    f"{path.relative_to(FORGE_DIR)}: domain='{file_domain}' "
                    f"but parent dir='{parent_dir}'"
                )
        assert not mismatches, (
            f"Domain field mismatches:\n"
            + "\n".join(f"  - {m}" for m in mismatches)
        )


# ── loadingStrategy enum validation ──────────────────────────────────

class TestLoadingStrategyEnum:
    """loadingStrategy must be one of the allowed values."""

    VALID_STRATEGIES = {"always", "onDemand", "lazy"}

    def test_all_loading_strategies_valid(self):
        """Every file's loadingStrategy should be in the allowed enum."""
        invalid = []
        for path, fm in _get_context_files_with_frontmatter():
            strategy = fm.get("loadingStrategy", "")
            if strategy and strategy not in self.VALID_STRATEGIES:
                invalid.append(
                    f"{path.relative_to(FORGE_DIR)}: "
                    f"loadingStrategy='{strategy}'"
                )
        assert not invalid, (
            f"Files with invalid loadingStrategy:\n"
            + "\n".join(f"  - {i}" for i in invalid)
        )


# ── All context files have required frontmatter fields ───────────────

class TestRequiredFrontmatterFields:
    """All context files must have the essential frontmatter fields."""

    REQUIRED_FIELDS = ["id", "domain", "title", "type", "estimatedTokens", "loadingStrategy"]

    def test_all_context_files_have_required_fields(self):
        """Every context .md file should have all required frontmatter fields."""
        missing_fields = []
        for domain_dir in _get_domain_dirs():
            for md_file in domain_dir.glob("*.md"):
                fm = extract_yaml_frontmatter(md_file)
                if fm is None:
                    missing_fields.append(
                        f"{md_file.relative_to(FORGE_DIR)}: NO frontmatter"
                    )
                    continue
                for field in self.REQUIRED_FIELDS:
                    if field not in fm:
                        missing_fields.append(
                            f"{md_file.relative_to(FORGE_DIR)}: missing '{field}'"
                        )
        assert not missing_fields, (
            f"Context files with missing required fields:\n"
            + "\n".join(f"  - {m}" for m in missing_fields)
        )


# ── Top-level context files ──────────────────────────────────────────

class TestTopLevelContextFiles:
    """Top-level context files (cross_domain.md, loading_protocol.md) exist."""

    def test_cross_domain_exists(self):
        assert (CONTEXT_DIR / "cross_domain.md").exists()

    def test_loading_protocol_exists(self):
        assert (CONTEXT_DIR / "loading_protocol.md").exists()

    def test_context_index_exists(self):
        assert (CONTEXT_DIR / "index.md").exists()

    def test_cross_domain_has_frontmatter(self):
        fm = extract_yaml_frontmatter(CONTEXT_DIR / "cross_domain.md")
        assert fm is not None, "cross_domain.md should have valid frontmatter"

    def test_loading_protocol_has_frontmatter(self):
        fm = extract_yaml_frontmatter(CONTEXT_DIR / "loading_protocol.md")
        assert fm is not None, "loading_protocol.md should have valid frontmatter"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
