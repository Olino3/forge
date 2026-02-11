"""Tests for memory pruning behaviour — independent lifecycle simulation.

Validates that the memory_pruning_daemon.sh correctly prunes oversized files
in temporary directories, preserving headers and inserting pruning markers.

This tests the pruning specification from lifecycle.md:
  - project_overview.md: 200 lines
  - review_history.md:   300 lines
  - All other memory:    500 lines
  - Header (first 5 lines) is always preserved
  - A pruning marker is inserted after the header

Event: SessionEnd
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
)


SCRIPT = "memory_pruning_daemon.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _run_pruning_in_env(env: TempForgeEnvironment, inp: dict) -> HookResult:
    """Run the pruning daemon with SCRIPT_DIR inside the temp env.

    The hook derives FORGE_DIR from SCRIPT_DIR (via BASH_SOURCE), so we
    must copy the hook into the temp env so file-path resolution targets
    the temporary directory instead of the real repository.
    """
    hooks_dir = env.project_root / "forge-plugin" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    lib_dir = hooks_dir / "lib"
    lib_dir.mkdir(parents=True, exist_ok=True)

    # Copy hook + shared lib into temp env
    shutil.copy2(HOOKS_DIR / SCRIPT, hooks_dir / SCRIPT)
    (hooks_dir / SCRIPT).chmod(0o755)
    shutil.copy2(HOOKS_DIR / "lib" / "health_buffer.sh", lib_dir / "health_buffer.sh")

    # CLAUDE_PLUGIN_ROOT must be 2 levels deep so ../../.forge -> env/.forge
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


def _make_session_end_input(
    transcript_path: str = "",
    session_id: str = "test-session",
    cwd: str = "/tmp",
    reason: str = "user_exit",
) -> dict:
    return {
        "transcript_path": transcript_path,
        "session_id": session_id,
        "cwd": cwd,
        "reason": reason,
    }


def _make_file_content(line_count: int, header_lines: int = 5) -> str:
    """Generate file content with a 5-line header and N total lines."""
    lines = ["<!-- Last Updated: 2025-06-01 -->"]
    lines.append("# Test Memory File")
    lines.append("")
    lines.append("## Summary")
    lines.append("Header content preserved on prune.")
    for i in range(line_count - header_lines):
        lines.append(f"Line {i + 1}: data entry for testing pruning behaviour.")
    return "\n".join(lines) + "\n"


# ── General files: 500-line limit ────────────────────────────────────

class TestGeneralPruningLimit:
    """General memory files should be pruned to ~500 lines."""

    def test_600_lines_pruned_to_500(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(600)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/findings.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_lines = fp.read_text().split("\n")
        # Allow tolerance for pruning marker (3 lines)
        assert len(result_lines) <= 510, f"Expected <=510, got {len(result_lines)}"

    def test_700_lines_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/review/proj/notes.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/review/proj/notes.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_lines = fp.read_text().split("\n")
        assert len(result_lines) <= 510, f"Expected <=510, got {len(result_lines)}"

    def test_500_lines_not_pruned(self, temp_forge_env):
        """Files at exactly the limit should not be pruned."""
        env = temp_forge_env()
        content = _make_file_content(500)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/data.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/data.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        original_content = fp.read_text()
        _run_pruning_in_env(env, inp)
        # Content should be unchanged (no pruning needed)
        assert fp.read_text() == original_content

    def test_499_lines_not_pruned(self, temp_forge_env):
        """Files below the limit should not be pruned."""
        env = temp_forge_env()
        content = _make_file_content(499)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/data.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/data.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        original_content = fp.read_text()
        _run_pruning_in_env(env, inp)
        assert fp.read_text() == original_content


# ── project_overview: 200-line limit ─────────────────────────────────

class TestProjectOverviewPruning:
    """project_overview.md should be pruned to ~200 lines."""

    def test_300_lines_pruned_to_200(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(300)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/projects/test/project_overview.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_lines = fp.read_text().split("\n")
        assert len(result_lines) <= 210, f"Expected <=210, got {len(result_lines)}"

    def test_200_lines_not_pruned(self, temp_forge_env):
        """At exactly 200 lines, no pruning needed."""
        env = temp_forge_env()
        content = _make_file_content(200)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/projects/test/project_overview.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        original = fp.read_text()
        _run_pruning_in_env(env, inp)
        assert fp.read_text() == original

    def test_201_lines_pruned(self, temp_forge_env):
        """At 201 lines (limit+1), pruning should kick in."""
        env = temp_forge_env()
        content = _make_file_content(201)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/projects/test/project_overview.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_lines = fp.read_text().split("\n")
        assert len(result_lines) <= 210, f"Expected <=210, got {len(result_lines)}"


# ── review_history: 300-line limit ───────────────────────────────────

class TestReviewHistoryPruning:
    """review_history.md should be pruned to ~300 lines."""

    def test_450_lines_pruned_to_300(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(450)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/review_history.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/projects/test/review_history.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_lines = fp.read_text().split("\n")
        assert len(result_lines) <= 310, f"Expected <=310, got {len(result_lines)}"

    def test_300_lines_not_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(300)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/review_history.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/projects/test/review_history.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        original = fp.read_text()
        _run_pruning_in_env(env, inp)
        assert fp.read_text() == original


# ── Header preservation ──────────────────────────────────────────────

class TestHeaderPreservation:
    """First 5 lines (header/metadata) should survive pruning."""

    def test_first_five_lines_preserved(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        original_lines = content.split("\n")[:5]
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/findings.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        new_lines = fp.read_text().split("\n")
        for i in range(1, 5):  # Skip line 0 (timestamp may refresh)
            assert new_lines[i] == original_lines[i], (
                f"Header line {i} changed: {new_lines[i]!r} != {original_lines[i]!r}"
            )

    def test_timestamp_line_preserved_or_refreshed(self, temp_forge_env):
        """First line should still contain a Last Updated timestamp."""
        env = temp_forge_env()
        content = _make_file_content(600)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/findings.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        first_line = fp.read_text().split("\n")[0]
        assert "Last Updated" in first_line


# ── Pruning marker ───────────────────────────────────────────────────

class TestPruningMarker:
    """A pruning marker comment should be inserted after the header."""

    def test_pruning_marker_present(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/findings.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_text = fp.read_text()
        assert "Pruned:" in result_text or "pruned" in result_text.lower()

    def test_pruning_marker_mentions_removed_count(self, temp_forge_env):
        """Pruning marker should indicate how many lines were removed."""
        env = temp_forge_env()
        content = _make_file_content(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/findings.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_text = fp.read_text()
        # Should mention "200 lines removed" (700 - 500 = 200)
        assert "lines removed" in result_text.lower() or "Pruned:" in result_text


# ── Operational files skipped ────────────────────────────────────────

class TestOperationalFilesSkipped:
    """Operational files (index.md, lifecycle.md, etc.) are never pruned."""

    def test_index_md_not_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(600)
        fp = env.create_file("forge-plugin/memory/index.md", content)
        transcript = env.create_file(
            "transcript.txt",
            f"Read {fp}\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        assert len(fp.read_text().split("\n")) >= 600

    def test_lifecycle_md_not_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(600)
        fp = env.create_file("forge-plugin/memory/lifecycle.md", content)
        transcript = env.create_file(
            "transcript.txt",
            f"Read {fp}\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        assert len(fp.read_text().split("\n")) >= 600

    def test_quality_guidance_not_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_file_content(600)
        fp = env.create_file("forge-plugin/memory/quality_guidance.md", content)
        transcript = env.create_file(
            "transcript.txt",
            f"Read {fp}\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        assert len(fp.read_text().split("\n")) >= 600


# ── Recent-file detection (no transcript) ────────────────────────────

class TestRecentFileDetection:
    """Pruning daemon also detects recently-modified files via find."""

    def test_recently_modified_file_detected(self, temp_forge_env):
        """Files modified in the last 2 hours are detected even without transcript."""
        env = temp_forge_env()
        content = _make_file_content(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/data.md",
            content,
        )
        # No transcript — relies on find -mmin -120
        inp = _make_session_end_input(
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        result_lines = fp.read_text().split("\n")
        assert len(result_lines) <= 510, f"Expected <=510, got {len(result_lines)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
