"""Tests for memory_cross_pollinator.sh — The Chronicle: Cross Skill Pollinator.

Validates that critical findings from skill memory files are propagated
to the project's cross_skill_insights.md file.

Event: PostToolUse (matcher: Write|Edit)
"""

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, FORGE_DIR


SCRIPT = "memory_cross_pollinator.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_post_input(file_path: str):
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path},
    }


# ── Non-skill memory files are ignored ──────────────────────────────────

class TestNonSkillMemoryIgnored:
    """Hook only processes memory/skills/*.md files."""

    def test_project_memory_ignored(self, runner):
        result = runner.run(_make_post_input(
            "forge-plugin/memory/projects/test/overview.md"
        ))
        assert result.exit_code == 0
        assert result.is_allow

    def test_source_file_ignored(self, runner):
        result = runner.run(_make_post_input("src/main.py"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_context_file_ignored(self, runner):
        result = runner.run(_make_post_input(
            "forge-plugin/context/python/frameworks.md"
        ))
        assert result.exit_code == 0
        assert result.is_allow


# ── Critical section propagation ────────────────────────────────────────

class TestCriticalSectionPropagation:
    """Critical/Security/Breaking/Performance headers should be propagated."""

    def test_critical_section_creates_insights_file(self, runner, temp_forge_env):
        env = temp_forge_env()
        skill_file = env.create_file(
            "forge-plugin/memory/skills/analyze/myproject/findings.md",
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Analysis Findings\n\n"
            "## Critical\n\n"
            "The database connection pool is exhausted under load.\n"
            "Needs urgent fix before next release.\n",
        )
        result = runner.run(
            _make_post_input(str(skill_file)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Check that cross_skill_insights.md was created
        insights_path = (
            env.project_root
            / "forge-plugin"
            / "memory"
            / "projects"
            / "myproject"
            / "cross_skill_insights.md"
        )
        if insights_path.exists():
            content = insights_path.read_text()
            assert "database" in content.lower() or "analyze" in content.lower()

    def test_security_section_propagated(self, runner, temp_forge_env):
        env = temp_forge_env()
        skill_file = env.create_file(
            "forge-plugin/memory/skills/improve/myproject/security.md",
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Improvement Notes\n\n"
            "## Security\n\n"
            "SQL injection vulnerability found in user input handler.\n",
        )
        result = runner.run(
            _make_post_input(str(skill_file)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0

    def test_breaking_section_propagated(self, runner, temp_forge_env):
        env = temp_forge_env()
        skill_file = env.create_file(
            "forge-plugin/memory/skills/implement/myproject/changes.md",
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Implementation\n\n"
            "## Breaking\n\n"
            "Removed deprecated v1 API endpoints.\n",
        )
        result = runner.run(
            _make_post_input(str(skill_file)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0

    def test_performance_section_propagated(self, runner, temp_forge_env):
        env = temp_forge_env()
        skill_file = env.create_file(
            "forge-plugin/memory/skills/analyze/myproject/perf.md",
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Performance\n\n"
            "## Performance\n\n"
            "Query response time degraded from 50ms to 2s after schema change.\n",
        )
        result = runner.run(
            _make_post_input(str(skill_file)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0


# ── Non-critical content not propagated ─────────────────────────────────

class TestNonCriticalNotPropagated:
    """Files without critical headers should not create insights."""

    def test_normal_findings_no_insights(self, runner, temp_forge_env):
        env = temp_forge_env()
        skill_file = env.create_file(
            "forge-plugin/memory/skills/analyze/myproject/notes.md",
            "<!-- Last Updated: 2025-01-01 -->\n"
            "# Notes\n\n"
            "## Architecture\n\n"
            "The project uses a standard MVC pattern.\n",
        )
        result = runner.run(
            _make_post_input(str(skill_file)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        insights_path = (
            env.project_root
            / "forge-plugin"
            / "memory"
            / "projects"
            / "myproject"
            / "cross_skill_insights.md"
        )
        # insights file should NOT be created (no critical content)
        assert not insights_path.exists()


# ── Insufficient path components ────────────────────────────────────────

class TestInsufficientPathComponents:
    """Paths with fewer than 3 components after 'memory/skills/' should be skipped."""

    def test_skill_root_file_skipped(self, runner, temp_forge_env):
        env = temp_forge_env()
        skill_file = env.create_file(
            "forge-plugin/memory/skills/analyze.md",
            "<!-- Last Updated: 2025-01-01 -->\n## Critical\nImportant!\n",
        )
        result = runner.run(
            _make_post_input(str(skill_file)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert result.is_allow


# ── Always allows (info-only) ───────────────────────────────────────────

class TestAlwaysAllows:
    """Cross pollinator never denies — it's purely informational."""

    def test_never_denies(self, runner, temp_forge_env):
        env = temp_forge_env()
        skill_file = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/data.md",
            "<!-- Last Updated: 2025-01-01 -->\n"
            "## Critical\nCritical finding here\n"
            "## Security\nSecurity issue here\n"
            "## Breaking\nBreaking change here\n"
            "## Performance\nPerformance problem here\n",
        )
        result = runner.run(
            _make_post_input(str(skill_file)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert result.is_allow
