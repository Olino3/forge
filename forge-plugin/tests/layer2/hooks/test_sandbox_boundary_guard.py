"""Tests for sandbox_boundary_guard.sh — The Shield: Host Isolation Guard.

Validates that file operations and bash commands are properly sandboxed
to the project directory, blocking access to sensitive system paths and
credential files.

Event: PreToolUse (matcher: Bash, Read, Write|Edit)
"""

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, FORGE_DIR, REPO_ROOT


SCRIPT = "sandbox_boundary_guard.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


# ── Helpers ─────────────────────────────────────────────────────────────────

def make_read_input(file_path: str, cwd: str | None = None):
    return {
        "tool_name": "Read",
        "tool_input": {"file_path": file_path},
        "cwd": cwd or str(REPO_ROOT),
    }


def make_write_input(file_path: str, cwd: str | None = None):
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path},
        "cwd": cwd or str(REPO_ROOT),
    }


def make_edit_input(file_path: str, cwd: str | None = None):
    return {
        "tool_name": "Edit",
        "tool_input": {"file_path": file_path},
        "cwd": cwd or str(REPO_ROOT),
    }


def make_bash_input(command: str, cwd: str | None = None):
    return {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": cwd or str(REPO_ROOT),
    }


# ── Read/Write/Edit: Project-internal paths (ALLOW) ────────────────────────

class TestSandboxAllowProjectPaths:
    """File operations within the project directory should be allowed."""

    def test_read_relative_path(self, runner):
        result = runner.run(make_read_input("src/main.py"))
        assert result.is_allow, f"Expected allow, got deny: {result.deny_reason}"

    def test_read_absolute_project_path(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/src/main.py"))
        assert result.is_allow

    def test_write_project_file(self, runner):
        result = runner.run(make_write_input(f"{REPO_ROOT}/output.txt"))
        assert result.is_allow

    def test_edit_project_file(self, runner):
        result = runner.run(make_edit_input(f"{REPO_ROOT}/README.md"))
        assert result.is_allow

    def test_read_tmp_path(self, runner):
        """Operations in /tmp should be allowed."""
        result = runner.run(make_read_input("/tmp/test_output.txt"))
        assert result.is_allow

    def test_read_var_tmp(self, runner):
        result = runner.run(make_read_input("/var/tmp/cache.dat"))
        assert result.is_allow

    def test_read_dev_null(self, runner):
        result = runner.run(make_read_input("/dev/null"))
        assert result.is_allow

    def test_no_file_path(self, runner):
        """Missing file_path should be allowed (nothing to check)."""
        result = runner.run({
            "tool_name": "Read",
            "tool_input": {},
            "cwd": str(REPO_ROOT),
        })
        assert result.is_allow


# ── Read/Write/Edit: Outside project paths (DENY) ──────────────────────────

class TestSandboxDenyOutsidePaths:
    """File operations outside the project directory should be denied."""

    def test_read_etc_passwd(self, runner):
        result = runner.run(make_read_input("/etc/passwd"))
        assert result.is_deny
        assert "outside the project directory" in result.deny_reason

    def test_read_ssh_key(self, runner):
        result = runner.run(make_read_input("/home/user/.ssh/id_rsa"))
        assert result.is_deny

    def test_write_etc_hosts(self, runner):
        result = runner.run(make_write_input("/etc/hosts"))
        assert result.is_deny

    def test_edit_bashrc(self, runner):
        result = runner.run(make_edit_input("/home/user/.bashrc"))
        assert result.is_deny

    def test_read_home_directory(self, runner):
        result = runner.run(make_read_input("/home/user/other-project/secrets.py"))
        assert result.is_deny


# ── Read/Write/Edit: Sensitive files even inside project (DENY) ────────────

class TestSandboxDenySensitiveFiles:
    """Sensitive credential files should be denied even inside the project."""

    def test_env_file(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/.env"))
        assert result.is_deny
        assert "secrets" in result.deny_reason.lower() or "credentials" in result.deny_reason.lower()

    def test_env_local_file(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/.env.local"))
        assert result.is_deny

    def test_pem_file(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/certs/server.pem"))
        assert result.is_deny

    def test_key_file(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/ssl/private.key"))
        assert result.is_deny

    def test_npmrc_file(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/.npmrc"))
        assert result.is_deny

    def test_pypirc_file(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/.pypirc"))
        assert result.is_deny

    def test_credentials_json(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/credentials.json"))
        assert result.is_deny

    def test_service_account_json(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/service-account-key.json"))
        assert result.is_deny

    def test_netrc(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/.netrc"))
        assert result.is_deny

    def test_git_credentials(self, runner):
        result = runner.run(make_read_input(f"{REPO_ROOT}/.git-credentials"))
        assert result.is_deny


# ── Bash commands: safe (ALLOW) ─────────────────────────────────────────────

class TestSandboxBashAllow:
    """Safe bash commands should be allowed."""

    def test_ls_command(self, runner):
        result = runner.run(make_bash_input("ls -la src/"))
        assert result.is_allow

    def test_python_command(self, runner):
        result = runner.run(make_bash_input("python3 -c 'print(1+1)'"))
        assert result.is_allow

    def test_echo_command(self, runner):
        result = runner.run(make_bash_input("echo hello"))
        assert result.is_allow

    def test_grep_project_files(self, runner):
        result = runner.run(make_bash_input("grep -r 'TODO' src/"))
        assert result.is_allow

    def test_empty_command(self, runner):
        """Empty command should be allowed (nothing to check)."""
        result = runner.run({
            "tool_name": "Bash",
            "tool_input": {"command": ""},
            "cwd": str(REPO_ROOT),
        })
        assert result.is_allow

    def test_non_bash_tool(self, runner):
        """Non-bash/read/write tool types should pass through."""
        result = runner.run({
            "tool_name": "Search",
            "tool_input": {"query": "test"},
            "cwd": str(REPO_ROOT),
        })
        assert result.is_allow


# ── Bash commands: dangerous paths (DENY) ───────────────────────────────────

class TestSandboxBashDenyDangerousPaths:
    """Bash commands referencing sensitive system paths should be denied."""

    @pytest.mark.parametrize("path", [
        "~/.ssh",
        "~/.gnupg",
        "~/.config",
        "~/.bashrc",
        "~/.bash_profile",
        "~/.zshrc",
        "~/.profile",
        "~/.aws",
        "~/.kube",
        "~/.docker",
        "$HOME/.ssh",
        "$HOME/.gnupg",
        "$HOME/.config",
        "$HOME/.aws",
    ])
    def test_dangerous_path_patterns(self, runner, path):
        result = runner.run(make_bash_input(f"cat {path}/config"))
        assert result.is_deny, f"Expected deny for path {path!r}, got allow"

    @pytest.mark.parametrize("path", [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/hosts",
        "/etc/sudoers",
    ])
    def test_system_file_patterns(self, runner, path):
        result = runner.run(make_bash_input(f"cat {path}"))
        assert result.is_deny


# ── Bash commands: sensitive file patterns (DENY) ───────────────────────────

class TestSandboxBashDenySensitivePatterns:
    """Bash commands referencing credential file patterns should be denied."""

    @pytest.mark.parametrize("pattern", [
        ".env",
        ".pem",
        ".key",
        ".p12",
        ".pfx",
        ".npmrc",
        ".pypirc",
        ".netrc",
        ".htpasswd",
        ".git-credentials",
        "credentials.json",
        "credentials.yaml",
        "service-account",
    ])
    def test_sensitive_file_in_bash(self, runner, pattern):
        result = runner.run(make_bash_input(f"cat project/{pattern}"))
        assert result.is_deny, f"Expected deny for pattern {pattern!r}"

    def test_rm_rf_root(self, runner):
        """Destructive 'rm -rf /' should be denied."""
        result = runner.run(make_bash_input("rm -rf /"))
        assert result.is_deny


# ── Exit code behavior ─────────────────────────────────────────────────────

class TestSandboxExitCodes:
    """All exits should be 0 (deny is expressed via JSON, not exit code)."""

    def test_allow_exit_code(self, runner):
        result = runner.run(make_read_input("src/main.py"))
        assert result.exit_code == 0

    def test_deny_exit_code(self, runner):
        result = runner.run(make_read_input("/etc/passwd"))
        assert result.exit_code == 0

    def test_deny_has_json_output(self, runner):
        result = runner.run(make_read_input("/etc/passwd"))
        assert result.json_output is not None
        assert "hookSpecificOutput" in result.json_output
        assert result.json_output["hookSpecificOutput"]["permissionDecision"] == "deny"


# ── With TempForgeEnvironment ──────────────────────────────────────────────

class TestSandboxWithTempEnv:
    """Tests using a temporary project directory for isolation."""

    def test_project_internal_path_with_cwd(self, runner, temp_forge_env):
        env = temp_forge_env()
        env.create_file("src/app.py", "print('hello')")
        result = runner.run(make_read_input(
            f"{env.project_root}/src/app.py",
            cwd=str(env.project_root),
        ))
        assert result.is_allow

    def test_outside_path_with_cwd(self, runner, temp_forge_env):
        env = temp_forge_env()
        result = runner.run(make_read_input(
            "/etc/passwd",
            cwd=str(env.project_root),
        ))
        assert result.is_deny


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
