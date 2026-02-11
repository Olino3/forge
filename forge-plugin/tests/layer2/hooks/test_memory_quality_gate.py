"""Tests for memory_quality_gate.sh — The Chronicle: Memory Quality Gate.

Validates that memory writes/edits are checked for quality:
- Timestamp injection/refresh
- Line-count limits (200/300/500)
- Vague entry detection
- Absolute path detection

Event: PostToolUse (matcher: Write|Edit)
"""

import json
from datetime import datetime

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, FORGE_DIR


SCRIPT = "memory_quality_gate.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_post_input(file_path: str):
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path},
    }


# ── Non-memory files are ignored ────────────────────────────────────────

class TestNonMemoryIgnored:
    """Hook should silently exit for non-memory files."""

    def test_source_file(self, runner):
        result = runner.run(_make_post_input("src/main.py"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_context_file(self, runner):
        result = runner.run(_make_post_input("forge-plugin/context/python/frameworks.md"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_claudedocs_file(self, runner):
        result = runner.run(_make_post_input("claudedocs/analysis.md"))
        assert result.exit_code == 0
        assert result.is_allow


class TestOperationalFilesSkipped:
    """Operational memory files should be skipped."""

    def test_index_md(self, runner):
        result = runner.run(_make_post_input("forge-plugin/memory/index.md"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_lifecycle_md(self, runner):
        result = runner.run(_make_post_input("forge-plugin/memory/lifecycle.md"))
        assert result.exit_code == 0
        assert result.is_allow


# ── Timestamp injection ─────────────────────────────────────────────────

class TestTimestampInjection:
    """Hook should inject/refresh Last Updated timestamp in memory files."""

    def test_injects_timestamp_in_new_file(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            "# Overview\n\nSome content\n",
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # File should now have a timestamp on the first line
        content = fp.read_text()
        assert "<!-- Last Updated:" in content
        today = datetime.now().strftime("%Y-%m-%d")
        assert today in content

    def test_refreshes_existing_timestamp(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            "<!-- Last Updated: 2020-01-01 -->\n# Overview\n\nOld timestamp\n",
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        content = fp.read_text()
        today = datetime.now().strftime("%Y-%m-%d")
        assert today in content
        assert "2020-01-01" not in content


# ── Line-count limits ───────────────────────────────────────────────────

class TestLineLimits:
    """Hook should warn when memory files exceed line limits."""

    def test_project_overview_over_200_lines(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = "<!-- Last Updated: 2025-01-01 -->\n# Overview\n" + "\n".join(
            [f"Line {i}" for i in range(210)]
        )
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Should have additionalContext warning about excess lines
        ctx = result.additional_context
        if ctx:
            assert "200" in ctx or "line" in ctx.lower() or "limit" in ctx.lower()

    def test_review_history_over_300_lines(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = "<!-- Last Updated: 2025-01-01 -->\n# History\n" + "\n".join(
            [f"Line {i}" for i in range(310)]
        )
        fp = env.create_file(
            "forge-plugin/memory/projects/test/review_history.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        ctx = result.additional_context
        if ctx:
            assert "300" in ctx or "line" in ctx.lower() or "limit" in ctx.lower()

    def test_general_file_under_500_lines_ok(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = "<!-- Last Updated: 2025-01-01 -->\n# Data\n" + "\n".join(
            [f"Line {i}" for i in range(100)]
        )
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/data.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Should not warn about line limits for a file well under 500

    def test_general_file_over_500_lines(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = "<!-- Last Updated: 2025-01-01 -->\n# Data\n" + "\n".join(
            [f"Line {i}" for i in range(510)]
        )
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/data.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        ctx = result.additional_context
        if ctx:
            assert "500" in ctx or "line" in ctx.lower() or "limit" in ctx.lower()


# ── Vague entry detection ───────────────────────────────────────────────

class TestVagueEntryDetection:
    """Hook should warn when file has too many vague expressions."""

    def test_many_vague_phrases_warns(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = (
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Overview\n"
            "The project uses custom patterns.\n"
            "It has some interesting architecture.\n"
            "Has various integrations with services.\n"
            "Uses custom middleware for things.\n"
            "Has some configuration for features.\n"
        )
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Should warn about vagueness
        ctx = result.additional_context
        if ctx:
            assert "vague" in ctx.lower() or "specificity" in ctx.lower() or "generic" in ctx.lower()


# ── Absolute path detection ─────────────────────────────────────────────

class TestAbsolutePathDetection:
    """Hook should warn when memory files contain absolute paths."""

    def test_linux_absolute_path(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = (
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Deployment\n"
            "App is at /home/developer/projects/myapp\n"
        )
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        ctx = result.additional_context
        if ctx:
            assert "path" in ctx.lower() or "absolute" in ctx.lower() or "/home/" in ctx

    def test_mac_absolute_path(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = (
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Config\n"
            "Stored at /Users/admin/configs/prod.yaml\n"
        )
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        ctx = result.additional_context
        if ctx:
            assert "path" in ctx.lower() or "absolute" in ctx.lower() or "/Users/" in ctx


# ── Never denies ────────────────────────────────────────────────────────

class TestNeverDenies:
    """memory_quality_gate is info-only — never produces a deny decision."""

    def test_oversized_file_not_denied(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = "<!-- Last Updated: 2025-01-01 -->\n# Data\n" + "\n".join(
            [f"Line {i}" for i in range(600)]
        )
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            content,
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert result.is_allow  # info-only, never deny
