"""Tests for frontmatter_validator.sh — The Foreman: Frontmatter Validator.

Validates that context file writes/edits include proper YAML frontmatter
with required fields and valid enum values.

Event: PreToolUse (matcher: Write|Edit)
"""

import json

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, FORGE_DIR


SCRIPT = "frontmatter_validator.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_write_input(file_path: str, content: str = "", cwd: str | None = None):
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path, "content": content},
        "cwd": cwd or str(FORGE_DIR.parent),
    }


def _make_edit_input(file_path: str, cwd: str | None = None):
    return {
        "tool_name": "Edit",
        "tool_input": {"file_path": file_path},
        "cwd": cwd or str(FORGE_DIR.parent),
    }


VALID_FRONTMATTER = """---
id: test-context-file
domain: python
title: Test Context File
type: reference
estimatedTokens: 500
loadingStrategy: onDemand
tags: [python, testing]
---

# Test Context

Some content here.
"""

MISSING_FIELDS_FRONTMATTER = """---
id: incomplete
domain: python
---

# Missing Fields

Missing title, type, estimatedTokens, loadingStrategy.
"""

INVALID_DOMAIN_FRONTMATTER = """---
id: bad-domain
domain: javascript
title: Bad Domain
type: reference
estimatedTokens: 500
loadingStrategy: onDemand
---

# Bad Domain

Domain 'javascript' is not in allowed enum.
"""

INVALID_TYPE_FRONTMATTER = """---
id: bad-type
domain: python
title: Bad Type
type: invalid_type
estimatedTokens: 500
loadingStrategy: onDemand
---

# Bad Type
"""

INVALID_STRATEGY_FRONTMATTER = """---
id: bad-strategy
domain: python
title: Bad Strategy
type: reference
estimatedTokens: 500
loadingStrategy: immediate
---

# Bad Strategy
"""

NO_FRONTMATTER = """# No Frontmatter

This context file has no YAML frontmatter at all.
"""


# ── Non-context files are ignored ───────────────────────────────────────

class TestNonContextFilesIgnored:
    """Hook should silently pass non-context files."""

    def test_memory_file(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/memory/projects/test/overview.md",
            "# Overview\nContent\n",
        ))
        assert result.exit_code == 0
        assert result.is_allow

    def test_skill_file(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/skills/analyze/SKILL.md",
            "# Skill\nContent\n",
        ))
        assert result.exit_code == 0
        assert result.is_allow

    def test_source_file(self, runner):
        result = runner.run(_make_write_input(
            "src/main.py",
            "print('hello')\n",
        ))
        assert result.exit_code == 0
        assert result.is_allow


# ── Special context files are skipped ───────────────────────────────────

class TestSpecialContextFilesSkipped:
    """index.md, cross_domain.md, loading_protocol.md should be skipped."""

    def test_index_md_skipped(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/index.md",
            "# Index\nNo frontmatter needed\n",
        ))
        assert result.exit_code == 0
        assert result.is_allow

    def test_cross_domain_skipped(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/cross_domain.md",
            "# Cross Domain\nNo frontmatter\n",
        ))
        assert result.exit_code == 0
        assert result.is_allow

    def test_loading_protocol_skipped(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/loading_protocol.md",
            "# Loading Protocol\nNo frontmatter\n",
        ))
        assert result.exit_code == 0
        assert result.is_allow


# ── Valid frontmatter allowed ───────────────────────────────────────────

class TestValidFrontmatter:
    """Context files with correct frontmatter should be allowed."""

    def test_valid_write(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/python/test_context.md",
            VALID_FRONTMATTER,
        ))
        assert result.exit_code == 0
        assert result.is_allow

    def test_valid_all_domains(self, runner):
        domains = ["engineering", "angular", "azure", "commands", "dotnet",
                    "git", "python", "schema", "security"]
        for domain in domains:
            content = VALID_FRONTMATTER.replace("domain: python", f"domain: {domain}")
            result = runner.run(_make_write_input(
                f"forge-plugin/context/{domain}/test.md",
                content,
            ))
            assert result.is_allow, f"Domain '{domain}' should be valid"

    def test_valid_all_types(self, runner):
        types = ["always", "framework", "reference", "pattern", "index", "detection"]
        for t in types:
            content = VALID_FRONTMATTER.replace("type: reference", f"type: {t}")
            result = runner.run(_make_write_input(
                "forge-plugin/context/python/test.md",
                content,
            ))
            assert result.is_allow, f"Type '{t}' should be valid"

    def test_valid_all_strategies(self, runner):
        strategies = ["always", "onDemand", "lazy"]
        for strategy in strategies:
            content = VALID_FRONTMATTER.replace(
                "loadingStrategy: onDemand",
                f"loadingStrategy: {strategy}",
            )
            result = runner.run(_make_write_input(
                "forge-plugin/context/python/test.md",
                content,
            ))
            assert result.is_allow, f"Strategy '{strategy}' should be valid"


# ── Invalid frontmatter denied ──────────────────────────────────────────

class TestInvalidFrontmatterDenied:
    """Context files with invalid frontmatter should be denied."""

    def test_no_frontmatter_denied(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/python/test.md",
            NO_FRONTMATTER,
        ))
        assert result.is_deny

    def test_missing_fields_denied(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/python/test.md",
            MISSING_FIELDS_FRONTMATTER,
        ))
        assert result.is_deny

    def test_invalid_domain_denied(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/python/test.md",
            INVALID_DOMAIN_FRONTMATTER,
        ))
        assert result.is_deny

    def test_invalid_type_denied(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/python/test.md",
            INVALID_TYPE_FRONTMATTER,
        ))
        assert result.is_deny

    def test_invalid_strategy_denied(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/python/test.md",
            INVALID_STRATEGY_FRONTMATTER,
        ))
        assert result.is_deny

    def test_deny_reason_present(self, runner):
        result = runner.run(_make_write_input(
            "forge-plugin/context/python/test.md",
            NO_FRONTMATTER,
        ))
        assert result.is_deny
        assert result.deny_reason != ""


# ── Edit mode validates existing file ───────────────────────────────────

class TestEditMode:
    """Edit operations should validate existing file content."""

    def test_edit_valid_existing_file(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/context/python/test.md",
            VALID_FRONTMATTER,
        )
        result = runner.run(
            _make_edit_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # For edits, the hook checks the existing file; valid frontmatter → allow
        assert result.is_allow

    def test_edit_file_without_frontmatter(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/context/python/test.md",
            NO_FRONTMATTER,
        )
        result = runner.run(
            _make_edit_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Edit of a file missing frontmatter should deny
        assert result.is_deny
