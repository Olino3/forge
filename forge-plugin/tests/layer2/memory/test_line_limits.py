"""Tests for memory line limit enforcement — independent lifecycle simulation.

Validates the memory_quality_gate.sh line limit warnings at exact
boundaries defined in lifecycle.md:
  - project_overview.md: 200 lines
  - review_history.md:   300 lines
  - All other memory:    500 lines

The quality gate never denies writes — it only warns via additionalContext.

Event: PostToolUse (matcher: Write|Edit)
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from layer2.hooks.hook_helpers import (
    HookResult,
    HookRunner,
    TempForgeEnvironment,
    HOOKS_DIR,
    REPO_ROOT,
)


SCRIPT = "memory_quality_gate.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _run_quality_gate_in_env(
    env: TempForgeEnvironment, inp: dict
) -> HookResult:
    """Run quality gate with SCRIPT_DIR inside the temp env.

    Like memory_pruning_daemon, this hook derives FORGE_DIR from
    SCRIPT_DIR, so we copy it into the temp env for path resolution.
    """
    hooks_dir = env.project_root / "forge-plugin" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    lib_dir = hooks_dir / "lib"
    lib_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(HOOKS_DIR / SCRIPT, hooks_dir / SCRIPT)
    (hooks_dir / SCRIPT).chmod(0o755)
    shutil.copy2(HOOKS_DIR / "lib" / "health_buffer.sh", lib_dir / "health_buffer.sh")

    plugin_root = env.project_root / "_plugin" / "_level2"
    plugin_root.mkdir(parents=True, exist_ok=True)

    proc = subprocess.run(
        ["bash", str(hooks_dir / SCRIPT)],
        input=json.dumps(inp),
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(plugin_root)},
        cwd=str(env.project_root),
    )
    return HookResult(proc.returncode, proc.stdout, proc.stderr)


def _make_post_tool_input(file_path: str) -> dict:
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path},
    }


def _make_file_content(line_count: int) -> str:
    """Generate memory file content with N total lines."""
    lines = ["<!-- Last Updated: 2025-06-01 -->"]
    lines.append("# Test Memory File")
    lines.append("")
    lines.append("## Content")
    for i in range(line_count - 4):
        lines.append(f"Data line {i + 1}: specific project detail here.")
    return "\n".join(lines) + "\n"


# ── General files: 500-line limit ────────────────────────────────────

class TestGeneralLineLimits:
    """General memory files warn at >500 lines but not at <=500."""

    def test_500_lines_no_warning(self, temp_forge_env):
        """At exactly 500 lines, no warning should be issued."""
        env = temp_forge_env()
        content = _make_file_content(500)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        # Should not warn about exceeding limit
        ctx = result.additional_context.lower()
        assert "exceed" not in ctx or "500" not in ctx

    def test_499_lines_no_warning(self, temp_forge_env):
        """Below the limit — no warning."""
        env = temp_forge_env()
        content = _make_file_content(499)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        ctx = result.additional_context.lower()
        assert "exceed" not in ctx or "500" not in ctx

    def test_501_lines_warns(self, temp_forge_env):
        """At 501 lines (limit+1), warning should fire."""
        env = temp_forge_env()
        content = _make_file_content(501)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert result.has_warning
        ctx = result.additional_context.lower()
        assert "500" in ctx or "exceed" in ctx or "limit" in ctx

    def test_700_lines_warns(self, temp_forge_env):
        """Well over the limit — should warn."""
        env = temp_forge_env()
        content = _make_file_content(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/data.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert result.has_warning


# ── project_overview.md: 200-line limit ──────────────────────────────

class TestProjectOverviewLineLimits:
    """project_overview.md warns at >200 lines."""

    def test_200_lines_no_warning(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(200)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        ctx = result.additional_context.lower()
        assert "exceed" not in ctx or "200" not in ctx

    def test_201_lines_warns(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(201)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert result.has_warning
        ctx = result.additional_context.lower()
        assert "200" in ctx or "exceed" in ctx or "limit" in ctx

    def test_150_lines_no_warning(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(150)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        ctx = result.additional_context.lower()
        assert "exceed" not in ctx or "200" not in ctx


# ── review_history.md: 300-line limit ────────────────────────────────

class TestReviewHistoryLineLimits:
    """review_history.md warns at >300 lines."""

    def test_300_lines_no_warning(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(300)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/review_history.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        ctx = result.additional_context.lower()
        assert "exceed" not in ctx or "300" not in ctx

    def test_301_lines_warns(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(301)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/review_history.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert result.has_warning
        ctx = result.additional_context.lower()
        assert "300" in ctx or "exceed" in ctx or "limit" in ctx

    def test_250_lines_no_warning(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(250)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/review_history.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        ctx = result.additional_context.lower()
        assert "exceed" not in ctx or "300" not in ctx


# ── Never denies ─────────────────────────────────────────────────────

class TestNeverDenies:
    """Quality gate writes are advisory; it should never deny."""

    def test_oversized_file_not_denied(self, temp_forge_env):
        """Even a 1000-line file should be allowed (with warning)."""
        env = temp_forge_env()
        content = _make_file_content(1000)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/huge.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert result.is_allow  # never deny
        assert result.has_warning  # but should warn

    def test_oversized_project_overview_not_denied(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(400)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert result.is_allow


# ── Operational files skipped ────────────────────────────────────────

class TestOperationalFilesSkipped:
    """Operational files are not subject to line limit checks."""

    def test_index_md_skipped(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(600)
        fp = env.create_file("forge-plugin/memory/index.md", content)
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert not result.has_warning

    def test_lifecycle_md_skipped(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(600)
        fp = env.create_file("forge-plugin/memory/lifecycle.md", content)
        result = _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        assert result.exit_code == 0
        assert not result.has_warning


# ── Timestamp injection ──────────────────────────────────────────────

class TestTimestampInjection:
    """Quality gate should inject or refresh timestamps."""

    def test_injects_timestamp_when_missing(self, temp_forge_env):
        """A file without a timestamp should get one injected."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/findings.md",
            "# Findings\nSome data\n",
        )
        _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        first_line = fp.read_text().split("\n")[0]
        assert "Last Updated" in first_line

    def test_refreshes_old_timestamp(self, temp_forge_env):
        """An existing timestamp should be refreshed to today."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/findings.md",
            "<!-- Last Updated: 2024-01-01 -->\n# Findings\nSome data\n",
        )
        _run_quality_gate_in_env(env, _make_post_tool_input(str(fp)))
        first_line = fp.read_text().split("\n")[0]
        assert "Last Updated" in first_line
        # Should no longer be 2024-01-01
        assert "2024-01-01" not in first_line


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
