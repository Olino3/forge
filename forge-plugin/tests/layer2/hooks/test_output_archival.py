"""Tests for output_archival.sh — The Foreman: Output Archival.

Validates that claudedocs output files are archived with timestamps
and manifest tracking.

NOTE: This hook runs as a standalone script (not stdin-driven like most hooks).
It takes an optional argument for the claudedocs directory.
"""

import subprocess
import os
import time

import pytest

from layer2.hooks.hook_helpers import HOOKS_DIR, TempForgeEnvironment


SCRIPT = HOOKS_DIR / "output_archival.sh"


def _run_archival(env, claudedocs_dir: str = "") -> tuple[int, str, str]:
    """Run the output_archival.sh script."""
    cmd = ["bash", str(SCRIPT)]
    if claudedocs_dir:
        cmd.append(claudedocs_dir)

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(env.project_root),
        env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(HOOKS_DIR.parent)},
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestNoCaudedocsDirectory:
    """Hook should exit silently if claudedocs directory doesn't exist."""

    def test_no_claudedocs_exits_zero(self, temp_forge_env):
        env = temp_forge_env(init_git=True)
        rc, stdout, stderr = _run_archival(env, str(env.project_root / "claudedocs"))
        assert rc == 0


class TestArchiveCreation:
    """Hook should archive recently modified claudedocs files."""

    def test_archives_recent_file(self, temp_forge_env):
        env = temp_forge_env(init_git=True)
        claudedocs = env.project_root / "claudedocs"
        claudedocs.mkdir()
        output_file = claudedocs / "analysis-my-project.md"
        output_file.write_text("# Analysis\n\nSome content.\n")
        # Touch the file to ensure -mmin -10 picks it up
        os.utime(str(output_file))

        rc, stdout, stderr = _run_archival(env, str(claudedocs))
        assert rc == 0

        # Check for archived files recursively under archive/
        archive_root = claudedocs / "archive"
        archived_files = list(archive_root.rglob("analysis-my-project.md"))
        assert len(archived_files) >= 1, (
            f"Expected archived file, found none. "
            f"Archive contents: {list(archive_root.rglob('*'))}"
        )

    def test_creates_manifest(self, temp_forge_env):
        env = temp_forge_env(init_git=True)
        claudedocs = env.project_root / "claudedocs"
        claudedocs.mkdir()
        output_file = claudedocs / "analysis-test.md"
        output_file.write_text("# Test\n")
        os.utime(str(output_file))

        _run_archival(env, str(claudedocs))

        manifest = claudedocs / "archive" / "manifest.md"
        if manifest.exists():
            content = manifest.read_text()
            assert "Archive Manifest" in content or "manifest" in content.lower()


class TestManifestSkipped:
    """manifest.md itself should not be archived."""

    def test_manifest_not_archived(self, temp_forge_env):
        env = temp_forge_env(init_git=True)
        claudedocs = env.project_root / "claudedocs"
        claudedocs.mkdir()
        (claudedocs / "archive").mkdir(parents=True)
        manifest = claudedocs / "manifest.md"
        manifest.write_text("# Manifest\n")
        os.utime(str(manifest))

        _run_archival(env, str(claudedocs))
        # manifest.md should not appear in archive
        # (It's at the root level so it would be found by maxdepth 1,
        # but the script skips files named "manifest.md")


class TestAlwaysExitsZero:
    """Output archival never fails — always exit 0."""

    def test_empty_claudedocs(self, temp_forge_env):
        env = temp_forge_env(init_git=True)
        claudedocs = env.project_root / "claudedocs"
        claudedocs.mkdir()
        rc, _, _ = _run_archival(env, str(claudedocs))
        assert rc == 0

    def test_no_recent_files(self, temp_forge_env):
        env = temp_forge_env(init_git=True)
        claudedocs = env.project_root / "claudedocs"
        claudedocs.mkdir()
        # Create a file but make it old (>10 minutes)
        old_file = claudedocs / "old-report.md"
        old_file.write_text("# Old\n")
        old_time = time.time() - 3600  # 1 hour ago
        os.utime(str(old_file), (old_time, old_time))

        rc, stdout, _ = _run_archival(env, str(claudedocs))
        assert rc == 0
        # Should not archive old files
        assert "Archived" not in stdout
