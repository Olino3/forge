"""Test YAML frontmatter validation for all context files.

Validates:
- All context/**/*.md files have valid YAML frontmatter
- Required fields present: id, domain, title, type, estimatedTokens, loadingStrategy
- Enum values are valid for domain, type, loadingStrategy
- id matches pattern ^[a-z]+/[a-z_]+$
- estimatedTokens is positive integer
- File's domain field matches parent directory name
- Index files' indexedFiles[].path references resolve to existing files
- Frontmatter validates against context_metadata.schema.json

Phase 2 of the Forge Testing Architecture.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, extract_yaml_frontmatter, load_json


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_DOMAINS = {
    "engineering", "angular", "azure", "commands",
    "dotnet", "git", "python", "schema", "security",
}

VALID_TYPES = {"always", "framework", "reference", "pattern", "index", "detection"}

VALID_LOADING_STRATEGIES = {"always", "onDemand", "lazy"}

CONTEXT_DIR = FORGE_DIR / "context"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_context_files() -> list[tuple[str, Path]]:
    """Return (relative_id, path) for all .md files under context/."""
    files = sorted(CONTEXT_DIR.rglob("*.md"))
    return [
        (str(f.relative_to(CONTEXT_DIR)), f)
        for f in files
    ]


def _get_domain_context_files() -> list[tuple[str, Path]]:
    """Return (relative_id, path) for all .md files inside domain subdirectories."""
    files = []
    for domain_dir in sorted(CONTEXT_DIR.iterdir()):
        if domain_dir.is_dir() and domain_dir.name in VALID_DOMAINS:
            for f in sorted(domain_dir.rglob("*.md")):
                files.append((str(f.relative_to(CONTEXT_DIR)), f))
    return files


def _get_index_files() -> list[tuple[str, Path]]:
    """Return (relative_id, path) for all index.md files in domain dirs."""
    files = []
    for domain_dir in sorted(CONTEXT_DIR.iterdir()):
        if domain_dir.is_dir() and domain_dir.name in VALID_DOMAINS:
            idx = domain_dir / "index.md"
            if idx.exists():
                files.append((str(idx.relative_to(CONTEXT_DIR)), idx))
    return files


# ---------------------------------------------------------------------------
# Basic Frontmatter Existence Tests
# ---------------------------------------------------------------------------


class TestFrontmatterPresence:
    """Every context file must have YAML frontmatter."""

    def test_context_dir_exists(self):
        """context/ directory must exist."""
        assert CONTEXT_DIR.is_dir()

    def test_context_files_exist(self):
        """At least one context file must exist."""
        assert len(_get_context_files()) > 0

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_has_frontmatter(self, rel_path, filepath):
        """Every domain context file must have YAML frontmatter."""
        fm = extract_yaml_frontmatter(filepath)
        assert fm is not None, (
            f"{rel_path}: No YAML frontmatter found (must start with ---)"
        )


# ---------------------------------------------------------------------------
# Required Fields Tests
# ---------------------------------------------------------------------------


class TestFrontmatterRequiredFields:
    """Validate required fields in all domain context files."""

    REQUIRED_FIELDS = ["id", "domain", "title", "type", "estimatedTokens", "loadingStrategy"]

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_has_required_fields(self, rel_path, filepath):
        """Every context file must have all 6 required frontmatter fields."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip(f"{rel_path}: No frontmatter (covered by presence test)")
        missing = [f for f in self.REQUIRED_FIELDS if f not in fm]
        assert not missing, (
            f"{rel_path}: Missing required fields: {missing}"
        )


# ---------------------------------------------------------------------------
# Enum Validation Tests
# ---------------------------------------------------------------------------


class TestFrontmatterEnumValues:
    """Validate enum fields use correct values."""

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_domain_enum(self, rel_path, filepath):
        """domain must be a valid enum value."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        domain = fm.get("domain")
        assert domain in VALID_DOMAINS, (
            f"{rel_path}: domain '{domain}' not in {VALID_DOMAINS}"
        )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_type_enum(self, rel_path, filepath):
        """type must be a valid enum value."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        ftype = fm.get("type")
        assert ftype in VALID_TYPES, (
            f"{rel_path}: type '{ftype}' not in {VALID_TYPES}"
        )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_loading_strategy_enum(self, rel_path, filepath):
        """loadingStrategy must be a valid enum value."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        ls = fm.get("loadingStrategy")
        assert ls in VALID_LOADING_STRATEGIES, (
            f"{rel_path}: loadingStrategy '{ls}' not in {VALID_LOADING_STRATEGIES}"
        )


# ---------------------------------------------------------------------------
# Field Value Validation Tests
# ---------------------------------------------------------------------------


class TestFrontmatterFieldValues:
    """Validate individual field values and patterns."""

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_id_pattern(self, rel_path, filepath):
        """id must match pattern ^[a-z]+/[a-z_]+$."""
        import re

        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        fid = fm.get("id", "")
        assert re.match(r"^[a-z]+/[a-z_]+$", fid), (
            f"{rel_path}: id '{fid}' does not match pattern ^[a-z]+/[a-z_]+$"
        )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_estimated_tokens_positive(self, rel_path, filepath):
        """estimatedTokens must be a positive integer."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        tokens = fm.get("estimatedTokens")
        assert isinstance(tokens, int), (
            f"{rel_path}: estimatedTokens must be int, got {type(tokens).__name__}"
        )
        assert tokens >= 1, (
            f"{rel_path}: estimatedTokens must be >= 1, got {tokens}"
        )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_estimated_tokens_reasonable(self, rel_path, filepath):
        """estimatedTokens should be reasonable (< 10000)."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        tokens = fm.get("estimatedTokens", 0)
        assert tokens < 10000, (
            f"{rel_path}: estimatedTokens {tokens} seems unreasonably high (>= 10000)"
        )


# ---------------------------------------------------------------------------
# Domain Consistency Tests
# ---------------------------------------------------------------------------


class TestDomainConsistency:
    """Validate file's domain matches its parent directory."""

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_domain_matches_parent_dir(self, rel_path, filepath):
        """File's domain field must match its parent directory name."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        domain = fm.get("domain")
        parent_dir = filepath.parent.name
        assert domain == parent_dir, (
            f"{rel_path}: domain='{domain}' but parent dir is '{parent_dir}'"
        )


# ---------------------------------------------------------------------------
# Schema Compliance Tests
# ---------------------------------------------------------------------------


class TestSchemaCompliance:
    """Validate frontmatter against context_metadata.schema.json."""

    @pytest.fixture(scope="class")
    def schema(self):
        return load_json(
            FORGE_DIR / "interfaces" / "schemas" / "context_metadata.schema.json"
        )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_domain_context_files(),
        ids=[r for r, _ in _get_domain_context_files()],
    )
    def test_frontmatter_validates_schema(self, rel_path, filepath, schema):
        """Frontmatter must validate against context_metadata.schema.json."""
        from jsonschema import ValidationError, validate

        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        try:
            validate(instance=fm, schema=schema)
        except ValidationError as e:
            pytest.fail(
                f"{rel_path}: Schema violation — {e.message}"
            )


# ---------------------------------------------------------------------------
# Index File Tests
# ---------------------------------------------------------------------------


class TestIndexFiles:
    """Validate index files and their indexedFiles references."""

    def test_every_domain_has_index(self):
        """Every domain directory must have an index.md."""
        for domain_dir in sorted(CONTEXT_DIR.iterdir()):
            if domain_dir.is_dir() and domain_dir.name in VALID_DOMAINS:
                idx = domain_dir / "index.md"
                assert idx.exists(), (
                    f"context/{domain_dir.name}/: Missing index.md"
                )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_index_files(),
        ids=[r for r, _ in _get_index_files()],
    )
    def test_index_has_indexed_files(self, rel_path, filepath):
        """Index files should have indexedFiles array."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        assert "indexedFiles" in fm, (
            f"{rel_path}: Index file missing 'indexedFiles' array"
        )
        assert isinstance(fm["indexedFiles"], list), (
            f"{rel_path}: 'indexedFiles' must be a list"
        )
        assert len(fm["indexedFiles"]) > 0, (
            f"{rel_path}: 'indexedFiles' is empty"
        )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_index_files(),
        ids=[r for r, _ in _get_index_files()],
    )
    def test_indexed_files_paths_resolve(self, rel_path, filepath):
        """All indexedFiles[].path must resolve to existing files."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        indexed = fm.get("indexedFiles", [])
        parent_dir = filepath.parent
        for entry in indexed:
            path = entry.get("path", "")
            resolved = parent_dir / path
            assert resolved.exists(), (
                f"{rel_path}: indexedFiles path '{path}' does not exist "
                f"(expected at {resolved})"
            )

    @pytest.mark.parametrize(
        "rel_path,filepath",
        _get_index_files(),
        ids=[r for r, _ in _get_index_files()],
    )
    def test_indexed_files_have_required_fields(self, rel_path, filepath):
        """Each indexedFiles entry must have id, path, type, loadingStrategy."""
        fm = extract_yaml_frontmatter(filepath)
        if fm is None:
            pytest.skip("No frontmatter")
        indexed = fm.get("indexedFiles", [])
        required = {"id", "path", "type", "loadingStrategy"}
        for i, entry in enumerate(indexed):
            missing = required - set(entry.keys())
            assert not missing, (
                f"{rel_path}: indexedFiles[{i}] missing fields: {missing}"
            )


# ---------------------------------------------------------------------------
# Top-Level Context Files Tests
# ---------------------------------------------------------------------------


class TestTopLevelContextFiles:
    """Validate top-level context files (cross_domain.md, loading_protocol.md)."""

    def test_cross_domain_has_frontmatter(self):
        """cross_domain.md must have valid frontmatter."""
        path = CONTEXT_DIR / "cross_domain.md"
        if not path.exists():
            pytest.skip("cross_domain.md not found")
        fm = extract_yaml_frontmatter(path)
        assert fm is not None, "cross_domain.md: Missing frontmatter"
        assert "id" in fm
        assert "domain" in fm

    def test_loading_protocol_has_frontmatter(self):
        """loading_protocol.md must have valid frontmatter."""
        path = CONTEXT_DIR / "loading_protocol.md"
        if not path.exists():
            pytest.skip("loading_protocol.md not found")
        fm = extract_yaml_frontmatter(path)
        assert fm is not None, "loading_protocol.md: Missing frontmatter"
        assert "id" in fm
        assert "domain" in fm

    def test_top_level_index_exists(self):
        """context/index.md must exist."""
        assert (CONTEXT_DIR / "index.md").exists(), "context/index.md missing"

    def test_top_level_index_has_frontmatter(self):
        """context/index.md must have valid frontmatter."""
        path = CONTEXT_DIR / "index.md"
        fm = extract_yaml_frontmatter(path)
        assert fm is not None, "context/index.md: Missing frontmatter"


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
