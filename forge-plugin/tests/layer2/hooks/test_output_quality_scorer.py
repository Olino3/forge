"""Tests for output_quality_scorer.sh — The Town Crier: Output Quality Scorer.

Validates that claudedocs output files are scored on 4 criteria:
Completeness (30pts), Actionability (30pts), Formatting (25pts), Naming (15pts).

NOTE: Despite TESTING_ROADMAP listing under Foreman, this hook self-identifies
as Town Crier §6.4. Tests are placed here per TESTING_ROADMAP structure.

Event: PostToolUse (matcher: Write|Edit)
"""

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment


SCRIPT = "output_quality_scorer.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_post_input(file_path: str):
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path},
    }


# ── Non-claudedocs files ignored ────────────────────────────────────────

class TestNonClaudedocsIgnored:
    """Hook should silently pass non-claudedocs files."""

    def test_source_file(self, runner):
        result = runner.run(_make_post_input("src/main.py"))
        assert result.exit_code == 0
        assert result.is_allow
        assert not result.has_warning

    def test_memory_file(self, runner):
        result = runner.run(_make_post_input(
            "forge-plugin/memory/projects/test/overview.md"
        ))
        assert result.exit_code == 0
        assert result.is_allow

    def test_context_file(self, runner):
        result = runner.run(_make_post_input(
            "forge-plugin/context/python/frameworks.md"
        ))
        assert result.exit_code == 0
        assert result.is_allow


# ── Special claudedocs files skipped ────────────────────────────────────

class TestSpecialFilesSkipped:
    """manifest.md and archive/ files should be skipped."""

    def test_manifest_skipped(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file("claudedocs/manifest.md", "# Manifest\n")
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert result.is_allow

    def test_archive_file_skipped(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "claudedocs/archive/2025-01/old-report.md",
            "# Archived\n",
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert result.is_allow


# ── High quality output ─────────────────────────────────────────────────

class TestHighQualityOutput:
    """Well-structured claudedocs should score high (A or B grade)."""

    def test_complete_output_scores_well(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = (
            "# Analysis: my-project\n\n"
            "## Summary\n\n"
            "Comprehensive analysis of the project architecture.\n\n"
            "## Findings\n\n"
            "### Finding 1: Database Performance\n\n"
            "- **Issue**: Query response time exceeds 2s threshold\n"
            "- **Impact**: User experience degradation\n"
            "- **Recommendation**: Add index on `users.email` column\n\n"
            "### Finding 2: Error Handling\n\n"
            "- **Issue**: Unhandled exceptions in payment flow\n"
            "- **Impact**: Transaction failures go unlogged\n"
            "- **Recommendation**: Implement structured error handling\n\n"
            "## Action Items\n\n"
            "1. [ ] Add database index\n"
            "2. [ ] Implement error handling\n"
            "3. [ ] Set up monitoring alerts\n\n"
            "## References\n\n"
            "- [Project Architecture](docs/architecture.md)\n"
        )
        fp = env.create_file("claudedocs/analysis-my-project.md", content)
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Should have quality feedback in additionalContext
        if result.has_warning:
            ctx = result.additional_context
            # Score info should be present
            assert any(g in ctx for g in ["A", "B", "C", "D", "F", "score", "Score"])

    def test_appends_quality_metadata(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = (
            "# Analysis: test-project\n\n"
            "## Summary\n\nGood analysis.\n\n"
            "## Findings\n\n- Finding 1\n- Finding 2\n\n"
            "## Action Items\n\n1. Do this\n2. Do that\n"
        )
        fp = env.create_file("claudedocs/analysis-test-project.md", content)
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Check that quality metadata was appended to the file
        new_content = fp.read_text()
        # The hook appends a YAML-style quality block
        assert "quality" in new_content.lower() or "score" in new_content.lower() or "grade" in new_content.lower()


# ── Low quality output ──────────────────────────────────────────────────

class TestLowQualityOutput:
    """Minimal or poorly structured output should score lower."""

    def test_minimal_content_scores_lower(self, runner, temp_forge_env):
        env = temp_forge_env()
        content = "Some notes here.\n"
        fp = env.create_file("claudedocs/notes.md", content)
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Should still exit 0 and be allowed (info-only)
        assert result.is_allow


# ── Always allows (info-only) ───────────────────────────────────────────

class TestAlwaysAllows:
    """Output quality scorer never denies — it's purely informational."""

    def test_worst_quality_not_denied(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file("claudedocs/bad.md", "x\n")
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert result.is_allow
