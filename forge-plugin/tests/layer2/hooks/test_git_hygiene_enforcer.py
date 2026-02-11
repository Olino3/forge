"""Tests for git_hygiene_enforcer.sh — The Shield: Source Control Safety Guard.

Validates enforcement of safe git practices:
- Block direct push to protected branches (main/master)
- Block force push
- Enforce Conventional Commits format
- Scan staged diffs for secrets

Event: PreToolUse (matcher: Bash)
"""

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, REPO_ROOT


SCRIPT = "git_hygiene_enforcer.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


# ── Helpers ─────────────────────────────────────────────────────────────────

def make_bash_input(command: str, cwd: str | None = None):
    return {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": cwd or str(REPO_ROOT),
    }


# ── Push to protected branches (DENY) ──────────────────────────────────────

class TestGitHygienePushProtected:
    """Direct pushes to main/master should be denied."""

    @pytest.mark.parametrize("branch", ["main", "master"])
    def test_push_to_protected_branch(self, runner, branch):
        result = runner.run(make_bash_input(f"git push origin {branch}"))
        assert result.is_deny, f"Expected deny for push to {branch}"
        assert branch in result.deny_reason

    @pytest.mark.parametrize("branch", ["main", "master"])
    def test_push_head_to_protected(self, runner, branch):
        result = runner.run(make_bash_input(f"git push origin HEAD:{branch}"))
        assert result.is_deny

    def test_push_to_feature_branch_allowed(self, runner):
        result = runner.run(make_bash_input("git push origin feature-auth"))
        assert result.is_allow

    def test_push_to_develop_allowed(self, runner):
        result = runner.run(make_bash_input("git push origin develop"))
        assert result.is_allow


# ── Force push (DENY) ─────────────────────────────────────────────────────

class TestGitHygieneForcePush:
    """Force push should be denied regardless of branch."""

    def test_force_flag(self, runner):
        result = runner.run(make_bash_input("git push --force origin feature"))
        assert result.is_deny
        assert "force" in result.deny_reason.lower()

    def test_force_short_flag(self, runner):
        result = runner.run(make_bash_input("git push -f origin feature"))
        assert result.is_deny

    def test_force_with_lease(self, runner):
        result = runner.run(make_bash_input("git push --force-with-lease origin feature"))
        assert result.is_deny


# ── Conventional Commits (WARN) ────────────────────────────────────────────

class TestGitHygieneConventionalCommits:
    """Non-conventional commit messages should produce a warning."""

    @pytest.mark.parametrize("msg", [
        "feat: add login page",
        "fix: resolve null pointer in auth",
        "docs: update README",
        "chore: clean up imports",
        "refactor(auth): simplify token validation",
        "test: add unit tests for parser",
        "feat!: breaking change in API",
        "ci: update GitHub Actions workflow",
        "perf(db): optimize query performance",
        "build: upgrade webpack to v5",
    ])
    def test_conventional_commit_allowed(self, runner, msg):
        result = runner.run(make_bash_input(f'git commit -m "{msg}"'))
        assert not result.has_warning or "conventional" not in result.additional_context.lower(), \
            f"Unexpected warning for valid conventional commit: {msg!r}"

    @pytest.mark.parametrize("msg", [
        "updated stuff",
        "fix bug",
        "WIP",
        "changes",
        "asdf",
    ])
    def test_non_conventional_commit_warns(self, runner, msg):
        result = runner.run(make_bash_input(f'git commit -m "{msg}"'))
        # Should produce a warning (additionalContext) but NOT deny
        assert not result.is_deny, "Non-conventional commit should warn, not deny"
        assert result.has_warning, f"Expected warning for non-conventional commit: {msg!r}"
        assert "conventional" in result.additional_context.lower()


# ── Non-git commands (ALLOW) ───────────────────────────────────────────────

class TestGitHygieneNonGitCommands:
    """Non-git commands should pass through immediately."""

    def test_ls_command(self, runner):
        result = runner.run(make_bash_input("ls -la"))
        assert result.is_allow
        assert not result.has_warning

    def test_python_command(self, runner):
        result = runner.run(make_bash_input("python3 app.py"))
        assert result.is_allow

    def test_non_push_git_command(self, runner):
        """git commands that aren't push/commit should pass through."""
        result = runner.run(make_bash_input("git status"))
        assert result.is_allow

    def test_git_log(self, runner):
        result = runner.run(make_bash_input("git log --oneline -5"))
        assert result.is_allow

    def test_git_branch(self, runner):
        result = runner.run(make_bash_input("git branch -a"))
        assert result.is_allow

    def test_git_diff(self, runner):
        result = runner.run(make_bash_input("git diff HEAD~1"))
        assert result.is_allow

    def test_git_pull(self, runner):
        result = runner.run(make_bash_input("git pull origin develop"))
        assert result.is_allow


# ── Non-Bash tool types (ALLOW) ────────────────────────────────────────────

class TestGitHygieneNonBash:
    """Non-Bash tool types should pass through."""

    def test_read_tool(self, runner):
        result = runner.run({
            "tool_name": "Read",
            "tool_input": {"file_path": "src/main.py"},
        })
        assert result.is_allow

    def test_write_tool(self, runner):
        result = runner.run({
            "tool_name": "Write",
            "tool_input": {"file_path": "output.txt"},
        })
        assert result.is_allow


# ── Secrets in staged diff (DENY) ─────────────────────────────────────────

class TestGitHygieneSecretsInStagedDiff:
    """Commits with secrets in staged diffs should be denied."""

    def test_aws_key_in_staged_diff(self, runner, temp_forge_env):
        env = temp_forge_env(init_git=True)
        env.stage_file("config.py", 'AWS_KEY = "AKIA1234567890ABCDEF"')
        result = runner.run(
            make_bash_input('git commit -m "feat: add config"', cwd=str(env.project_root))
        )
        assert result.is_deny, "Expected deny for AWS key in staged diff"
        assert "secret" in result.deny_reason.lower() or "AKIA" in result.deny_reason

    def test_github_token_in_staged_diff(self, runner, temp_forge_env):
        env = temp_forge_env(init_git=True)
        env.stage_file("deploy.sh", 'TOKEN="ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl"')
        result = runner.run(
            make_bash_input('git commit -m "feat: add deploy"', cwd=str(env.project_root))
        )
        assert result.is_deny

    def test_private_key_in_staged_diff(self, runner, temp_forge_env):
        env = temp_forge_env(init_git=True)
        env.stage_file("key.txt", "-----BEGIN RSA PRIVATE KEY-----\nMIIEpA...")
        result = runner.run(
            make_bash_input('git commit -m "feat: add key"', cwd=str(env.project_root))
        )
        assert result.is_deny

    def test_clean_staged_diff(self, runner, temp_forge_env):
        env = temp_forge_env(init_git=True)
        env.stage_file("app.py", "print('hello world')")
        result = runner.run(
            make_bash_input('git commit -m "feat: add app"', cwd=str(env.project_root))
        )
        assert result.is_allow or (not result.is_deny), \
            f"Clean commit should not be denied: {result.deny_reason}"


# ── Exit code behavior ─────────────────────────────────────────────────────

class TestGitHygieneExitCodes:
    """All exits should be 0 (deny is via JSON)."""

    def test_allow_exit_0(self, runner):
        result = runner.run(make_bash_input("git push origin develop"))
        assert result.exit_code == 0

    def test_deny_exit_0(self, runner):
        result = runner.run(make_bash_input("git push origin main"))
        assert result.exit_code == 0

    def test_warn_exit_0(self, runner):
        result = runner.run(make_bash_input('git commit -m "bad message"'))
        assert result.exit_code == 0


# ── Chained commands ──────────────────────────────────────────────────────

class TestGitHygieneChainedCommands:
    """Git commands in command chains should still be checked."""

    def test_chained_push_to_main(self, runner):
        result = runner.run(make_bash_input("echo done && git push origin main"))
        assert result.is_deny

    def test_piped_push_to_main(self, runner):
        result = runner.run(make_bash_input("echo ok | git push origin main"))
        assert result.is_deny


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
