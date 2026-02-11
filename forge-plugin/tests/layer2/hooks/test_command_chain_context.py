"""Tests for command_chain_context.sh — The Foreman: Command Chain Context.

Validates that TaskCompleted events persist ExecutionContext state
to .forge/chain_state.json for command chaining.

Event: TaskCompleted
"""

import json

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment


SCRIPT = "command_chain_context.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_task_completed_input(
    task_id: str = "task-001",
    task_subject: str = "/analyze my-project",
    session_id: str = "session-001",
    cwd: str = "/tmp",
    transcript_path: str = "",
):
    return {
        "task_id": task_id,
        "task_subject": task_subject,
        "session_id": session_id,
        "cwd": cwd,
        "transcript_path": transcript_path,
    }


# ── No cwd exits silently ──────────────────────────────────────────────

class TestNoCwd:
    """Hook should exit silently if no cwd provided."""

    def test_no_cwd_exits_zero(self, runner):
        inp = {
            "task_id": "task-001",
            "task_subject": "/analyze test",
            "session_id": "session-001",
        }
        result = runner.run(inp)
        assert result.exit_code == 0


# ── Chain state file creation ───────────────────────────────────────────

class TestChainStateCreation:
    """First command should create .forge/chain_state.json."""

    def test_creates_chain_state_file(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="/analyze my-project",
        )
        result = runner.run(inp, cwd=str(env.project_root))
        assert result.exit_code == 0

        chain_state_path = env.forge_dir / "chain_state.json"
        assert chain_state_path.exists()

    def test_chain_state_is_valid_json(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="/analyze my-project",
        )
        runner.run(inp, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        assert "sessionId" in data
        assert "commandHistory" in data
        assert isinstance(data["commandHistory"], list)
        assert len(data["commandHistory"]) == 1

    def test_records_command_name(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="/analyze my-project",
        )
        runner.run(inp, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        assert data["commandHistory"][0]["command"] == "analyze"


# ── Command chaining (same session) ────────────────────────────────────

class TestCommandChaining:
    """Sequential commands in the same session should append to history."""

    def test_second_command_appended(self, runner, temp_forge_env):
        env = temp_forge_env()

        # First command
        inp1 = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="/analyze my-project",
            session_id="session-001",
        )
        runner.run(inp1, cwd=str(env.project_root))

        # Second command (same session)
        inp2 = _make_task_completed_input(
            task_id="task-002",
            cwd=str(env.project_root),
            task_subject="/implement feature-x",
            session_id="session-001",
        )
        runner.run(inp2, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        assert len(data["commandHistory"]) == 2
        assert data["commandHistory"][0]["command"] == "analyze"
        assert data["commandHistory"][1]["command"] == "implement"

    def test_third_command_appended(self, runner, temp_forge_env):
        env = temp_forge_env()

        for i, cmd in enumerate(["analyze", "implement", "test"], 1):
            inp = _make_task_completed_input(
                task_id=f"task-{i:03d}",
                cwd=str(env.project_root),
                task_subject=f"/{cmd} my-project",
                session_id="session-001",
            )
            runner.run(inp, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        assert len(data["commandHistory"]) == 3


# ── New session resets chain state ──────────────────────────────────────

class TestNewSessionResets:
    """A new session should start a fresh chain state."""

    def test_different_session_resets(self, runner, temp_forge_env):
        env = temp_forge_env()

        # Session 1
        inp1 = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="/analyze my-project",
            session_id="session-001",
        )
        runner.run(inp1, cwd=str(env.project_root))

        # Session 2 (different session_id)
        inp2 = _make_task_completed_input(
            task_id="task-002",
            cwd=str(env.project_root),
            task_subject="/implement feature",
            session_id="session-002",
        )
        runner.run(inp2, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        assert data["sessionId"] == "session-002"
        assert len(data["commandHistory"]) == 1


# ── Transcript data capture ─────────────────────────────────────────────

class TestTranscriptDataCapture:
    """Hook should extract context/memory/skill data from transcripts."""

    def test_captures_context_files(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/python/frameworks.md\n"
            "Tool: Read context/engineering/best_practices.md\n",
        )
        inp = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="/analyze my-project",
            transcript_path=str(transcript),
        )
        runner.run(inp, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        entry = data["commandHistory"][0]
        assert len(entry["contextLoaded"]) >= 1

    def test_captures_skills_invoked(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read skills/analyze/SKILL.md\n",
        )
        inp = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="/analyze my-project",
            transcript_path=str(transcript),
        )
        runner.run(inp, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        entry = data["commandHistory"][0]
        assert len(entry["skillsInvoked"]) >= 1
        assert "analyze" in entry["skillsInvoked"]


# ── Non-forge commands treated as generic ───────────────────────────────

class TestNonForgeCommands:
    """Non-forge task subjects should be recorded as 'task'."""

    def test_generic_task(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_task_completed_input(
            cwd=str(env.project_root),
            task_subject="fix the login bug",
        )
        runner.run(inp, cwd=str(env.project_root))

        chain_state_path = env.forge_dir / "chain_state.json"
        data = json.loads(chain_state_path.read_text())
        assert data["commandHistory"][0]["command"] == "task"


# ── Always exits 0 ─────────────────────────────────────────────────────

class TestAlwaysExitsZero:
    """Command chain context hook never blocks task completion."""

    def test_exits_zero(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_task_completed_input(cwd=str(env.project_root))
        result = runner.run(inp, cwd=str(env.project_root))
        assert result.exit_code == 0
