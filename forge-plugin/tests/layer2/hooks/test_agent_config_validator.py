"""Tests for agent_config_validator.sh — The Foreman: Agent Config Validator.

Validates agent configuration integrity on SubagentStart events.
Checks JSON validity, required fields, name matching, semver, etc.

NOTE: SubagentStart hooks CANNOT block — info-only via additionalContext.

Event: SubagentStart
"""

import json

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, FORGE_DIR


SCRIPT = "agent_config_validator.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_subagent_input(agent_type: str, agent_id: str = "agent-001"):
    return {
        "agent_type": agent_type,
        "agent_id": agent_id,
    }


# ── Built-in agents are skipped ─────────────────────────────────────────

class TestBuiltinAgentsSkipped:
    """Built-in agents (Bash, Explore, Plan) should be silently skipped."""

    def test_bash_agent_skipped(self, runner):
        result = runner.run(_make_subagent_input("Bash"))
        assert result.exit_code == 0
        assert result.is_allow
        assert not result.has_warning

    def test_explore_agent_skipped(self, runner):
        result = runner.run(_make_subagent_input("Explore"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_plan_agent_skipped(self, runner):
        result = runner.run(_make_subagent_input("Plan"))
        assert result.exit_code == 0
        assert result.is_allow


# ── Valid custom agents ─────────────────────────────────────────────────

class TestValidCustomAgents:
    """Known custom agents with valid configs should pass validation."""

    def test_python_engineer(self, runner):
        result = runner.run(_make_subagent_input("python-engineer"))
        assert result.exit_code == 0
        # Should have additionalContext with validation summary
        assert result.is_allow  # SubagentStart can never deny

    def test_hephaestus(self, runner):
        result = runner.run(_make_subagent_input("hephaestus"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_developer_environment_engineer(self, runner):
        result = runner.run(_make_subagent_input("developer-environment-engineer"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_full_stack_engineer(self, runner):
        result = runner.run(_make_subagent_input("full-stack-engineer"))
        assert result.exit_code == 0
        assert result.is_allow


# ── Invalid/unknown agents ──────────────────────────────────────────────

class TestInvalidAgents:
    """Unknown agents without config files should report issues."""

    def test_nonexistent_agent(self, runner):
        result = runner.run(_make_subagent_input("nonexistent-agent"))
        assert result.exit_code == 0
        # Should still exit 0 (SubagentStart cannot block)
        # But may have warning about missing config
        assert result.is_allow

    def test_empty_agent_type(self, runner):
        result = runner.run(_make_subagent_input(""))
        assert result.exit_code == 0
        assert result.is_allow


# ── Never blocks ────────────────────────────────────────────────────────

class TestNeverBlocks:
    """SubagentStart hooks cannot deny — they're purely informational."""

    def test_always_exits_zero(self, runner):
        result = runner.run(_make_subagent_input("any-random-agent"))
        assert result.exit_code == 0

    def test_never_deny(self, runner):
        result = runner.run(_make_subagent_input("nonexistent-agent"))
        assert result.is_allow  # Never deny for SubagentStart
