"""Tests for memory freshness lifecycle — independent of hooks.

Validates that memory files can be classified by age using the
``<!-- Last Updated: YYYY-MM-DD -->`` timestamp, and that the
30-day / 90-day boundaries defined in lifecycle.md are exact.

This tests the *specification* of freshness behaviour rather than a
specific hook script, using the memory_freshness_enforcer.sh as the
reference implementation.

Event: PreToolUse (matcher: Read)
"""

import json
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from layer2.hooks.hook_helpers import (
    HookResult,
    HookRunner,
    TempForgeEnvironment,
    HOOKS_DIR,
    REPO_ROOT,
)


SCRIPT = "memory_freshness_enforcer.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _date_str(days_ago: int) -> str:
    """Return a YYYY-MM-DD string for N days ago."""
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")


def _make_memory_content(days_ago: int, body: str = "# Test\nContent\n") -> str:
    """Create memory file content with a timestamp N days ago."""
    return f"<!-- Last Updated: {_date_str(days_ago)} -->\n{body}"


def _make_input(file_path: str, cwd: str | None = None) -> dict:
    return {
        "tool_name": "Read",
        "tool_input": {"file_path": file_path},
        "cwd": cwd or str(REPO_ROOT),
    }


# ── Fresh memory (0-30 days) ──────────────────────────────────────────

class TestFreshMemory:
    """Memory files updated within the last 30 days should be allowed."""

    def test_day_zero_is_fresh(self, runner, temp_forge_env):
        """Today's date should be classified as fresh."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(0),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow
        assert not result.has_warning

    def test_day_1_is_fresh(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/data.md",
            _make_memory_content(1),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow
        assert not result.has_warning

    def test_day_15_is_fresh(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/patterns.md",
            _make_memory_content(15),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow
        assert not result.has_warning

    def test_day_29_is_fresh(self, runner, temp_forge_env):
        """29 days is the last fresh day."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/skills/test/proj/data.md",
            _make_memory_content(29),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow
        assert not result.has_warning

    def test_day_30_is_fresh(self, runner, temp_forge_env):
        """30 days is still in the 0-30 range (fresh)."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(30),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow
        # Day 30 is the boundary — hook uses >= 31 for aging


# ── Aging memory (31-89 days) ─────────────────────────────────────────

class TestAgingMemory:
    """Memory files 31-89 days old should be allowed (hook writes to health buffer)."""

    def test_day_31_is_aging(self, runner, temp_forge_env):
        """31 days is the first aging day."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(31),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow
        # Hook writes to health_buffer, not stdout — verify allow

    def test_day_45_is_aging(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(45),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow

    def test_day_60_is_aging(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(60),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow

    def test_day_89_is_aging(self, runner, temp_forge_env):
        """89 days is the last aging day."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(89),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_allow


# ── Stale memory (90+ days) ──────────────────────────────────────────

class TestStaleMemory:
    """Memory files 90+ days old should be denied."""

    def test_day_90_is_stale(self, runner, temp_forge_env):
        """90 days is the first stale day (boundary)."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(90),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_deny

    def test_day_91_is_stale(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(91),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_deny

    def test_day_180_is_stale(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(180),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_deny

    def test_day_365_is_stale(self, runner, temp_forge_env):
        """A year-old memory should be denied."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(365),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_deny

    def test_stale_deny_reason_includes_age(self, runner, temp_forge_env):
        """Deny reason should mention the age or staleness."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            _make_memory_content(100),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.is_deny
        reason = result.deny_reason.lower()
        assert "100" in reason or "stale" in reason or "90" in reason


# ── Boundary precision ───────────────────────────────────────────────

class TestBoundaryPrecision:
    """Exact boundary days must classify correctly (30→fresh, 31→aging, 89→aging, 90→stale)."""

    def test_boundary_fresh_to_aging(self, runner, temp_forge_env):
        """Day 30 is fresh, day 31 transitions to aging."""
        env = temp_forge_env()

        # Day 30 → fresh (allow, no deny, no warning)
        fp30 = env.create_file(
            "forge-plugin/memory/projects/b1/overview.md",
            _make_memory_content(30),
        )
        r30 = runner.run(_make_input(str(fp30)), cwd=str(env.project_root))
        assert r30.is_allow, "Day 30 should be fresh (allow)"

        # Day 31 → aging (allow, possibly with health buffer warning)
        fp31 = env.create_file(
            "forge-plugin/memory/projects/b2/overview.md",
            _make_memory_content(31),
        )
        r31 = runner.run(_make_input(str(fp31)), cwd=str(env.project_root))
        assert r31.is_allow, "Day 31 should be aging (allow)"

    def test_boundary_aging_to_stale(self, runner, temp_forge_env):
        """Day 89 is aging (allow), day 90 transitions to stale (deny)."""
        env = temp_forge_env()

        # Day 89 → aging (allow)
        fp89 = env.create_file(
            "forge-plugin/memory/projects/b3/overview.md",
            _make_memory_content(89),
        )
        r89 = runner.run(_make_input(str(fp89)), cwd=str(env.project_root))
        assert r89.is_allow, "Day 89 should be aging (allow)"

        # Day 90 → stale (deny)
        fp90 = env.create_file(
            "forge-plugin/memory/projects/b4/overview.md",
            _make_memory_content(90),
        )
        r90 = runner.run(_make_input(str(fp90)), cwd=str(env.project_root))
        assert r90.is_deny, "Day 90 should be stale (deny)"


# ── Missing timestamp ────────────────────────────────────────────────

class TestMissingTimestamp:
    """Memory files without a timestamp should be denied (ghost archive)."""

    def test_no_timestamp_denied(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            "# Overview\nNo timestamp here\n",
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_deny

    def test_wrong_format_timestamp_denied(self, runner, temp_forge_env):
        """A file with a non-standard timestamp format should be denied."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            "**Last Updated**: 2025-01-01\n# Overview\nContent\n",
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        # The hook only detects <!-- Last Updated: YYYY-MM-DD --> format
        assert result.is_deny

    def test_empty_file_denied(self, runner, temp_forge_env):
        """An empty memory file should be denied."""
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            "",
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.exit_code == 0
        assert result.is_deny

    def test_deny_reason_mentions_ghost_or_timestamp(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/test/overview.md",
            "# No timestamp\nContent only\n",
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.is_deny
        reason = result.deny_reason.lower()
        assert "ghost" in reason or "timestamp" in reason or "no" in reason


# ── Different memory paths ───────────────────────────────────────────

class TestDifferentMemoryPaths:
    """Freshness checks work across all memory subdirectories."""

    def test_shared_project_memory(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/projects/myproject/project_overview.md",
            _make_memory_content(10),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.is_allow

    def test_skill_specific_memory(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/skills/python-code-review/proj/review_history.md",
            _make_memory_content(5),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.is_allow

    def test_agent_memory(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/agents/hephaestus/notes.md",
            _make_memory_content(50),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.is_allow  # 50 days = aging, still allowed

    def test_command_memory(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "forge-plugin/memory/commands/myproject/analyze_history.md",
            _make_memory_content(95),
        )
        result = runner.run(_make_input(str(fp)), cwd=str(env.project_root))
        assert result.is_deny  # 95 days = stale


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
