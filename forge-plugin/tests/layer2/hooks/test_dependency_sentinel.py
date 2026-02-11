"""Tests for dependency_sentinel.sh — The Shield: Supply Chain Security Guard.

Validates that package install commands are checked against the deny list
in forge-plugin/security/deny_list.txt to block typosquatted or malicious
packages.

Event: PreToolUse (matcher: Bash)
"""

import pytest

from layer2.hooks.hook_helpers import HookRunner, FORGE_DIR


SCRIPT = "dependency_sentinel.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


# ── Helpers ─────────────────────────────────────────────────────────────────

def make_bash_input(command: str):
    return {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(FORGE_DIR.parent),
    }


# ── Prerequisite: deny list exists ──────────────────────────────────────────

class TestDenyListExists:
    """The deny list file must exist for the sentinel to function."""

    def test_deny_list_file_exists(self):
        deny_list = FORGE_DIR / "security" / "deny_list.txt"
        assert deny_list.exists(), "security/deny_list.txt not found"
        content = deny_list.read_text()
        assert len(content.strip()) > 0, "deny_list.txt is empty"


# ── pip install: safe packages (ALLOW) ──────────────────────────────────────

class TestDependencySentinelPipAllow:
    """Legitimate pip install commands should be allowed."""

    def test_pip_install_requests(self, runner):
        result = runner.run(make_bash_input("pip install requests"))
        assert result.is_allow, f"Unexpected deny: {result.deny_reason}"

    def test_pip_install_multiple_safe(self, runner):
        result = runner.run(make_bash_input("pip install requests flask pytest"))
        assert result.is_allow

    def test_pip_install_with_version(self, runner):
        result = runner.run(make_bash_input("pip install requests>=2.28.0"))
        assert result.is_allow

    def test_pip3_install(self, runner):
        result = runner.run(make_bash_input("pip3 install numpy"))
        assert result.is_allow

    def test_python_m_pip(self, runner):
        result = runner.run(make_bash_input("python -m pip install pandas"))
        assert result.is_allow

    def test_python3_m_pip(self, runner):
        result = runner.run(make_bash_input("python3 -m pip install django"))
        assert result.is_allow


# ── pip install: denied packages (DENY) ─────────────────────────────────────

class TestDependencySentinelPipDeny:
    """Typosquatted Python packages from the deny list should be blocked."""

    @pytest.mark.parametrize("package", [
        "colourama",
        "requestslib",
        "requsts",
        "requets",
        "urllib4",
        "djago",
        "djnago",
        "fask",
        "flsk",
        "nump",
        "numby",
        "pandsa",
    ])
    def test_pip_typosquat_denied(self, runner, package):
        result = runner.run(make_bash_input(f"pip install {package}"))
        assert result.is_deny, f"Expected deny for typosquat '{package}'"
        assert package.lower() in result.deny_reason.lower()

    def test_pip_deny_in_mixed_install(self, runner):
        """A deny-listed package mixed with legitimate ones should still be blocked."""
        result = runner.run(make_bash_input("pip install requests colourama flask"))
        assert result.is_deny
        assert "colourama" in result.deny_reason.lower()

    @pytest.mark.parametrize("package", [
        "ctx",
        "distutils-precedence",
        "pipconfig",
    ])
    def test_pip_known_malicious(self, runner, package):
        result = runner.run(make_bash_input(f"pip install {package}"))
        assert result.is_deny

    @pytest.mark.parametrize("package", [
        "setup",
        "pip",
        "os",
        "sys",
        "http",
    ])
    def test_pip_prefixed_suspicious(self, runner, package):
        """Packages with 'pip:' prefix in deny list should be caught."""
        result = runner.run(make_bash_input(f"pip install {package}"))
        assert result.is_deny, f"Expected deny for suspicious pip package '{package}'"


# ── npm install: safe packages (ALLOW) ──────────────────────────────────────

class TestDependencySentinelNpmAllow:
    """Legitimate npm install commands should be allowed."""

    def test_npm_install_express(self, runner):
        result = runner.run(make_bash_input("npm install express"))
        assert result.is_allow

    def test_npm_install_react(self, runner):
        result = runner.run(make_bash_input("npm install react react-dom"))
        assert result.is_allow

    def test_npm_i_shorthand(self, runner):
        result = runner.run(make_bash_input("npm i lodash"))
        assert result.is_allow


# ── npm install: denied packages (DENY) ─────────────────────────────────────

class TestDependencySentinelNpmDeny:
    """Typosquatted npm packages from the deny list should be blocked."""

    @pytest.mark.parametrize("package", [
        "crossenv",
        "cross-env.js",
        "lodahs",
        "loadsh",
        "expresss",
        "exress",
        "recat",
        "babelcli",
    ])
    def test_npm_typosquat_denied(self, runner, package):
        result = runner.run(make_bash_input(f"npm install {package}"))
        assert result.is_deny, f"Expected deny for npm typosquat '{package}'"

    @pytest.mark.parametrize("package", [
        "npm",
        "node",
        "kernel",
    ])
    def test_npm_prefixed_suspicious(self, runner, package):
        """Packages with 'npm:' prefix in deny list should be caught."""
        result = runner.run(make_bash_input(f"npm install {package}"))
        assert result.is_deny, f"Expected deny for suspicious npm package '{package}'"


# ── yarn add: denied packages (DENY) ────────────────────────────────────────

class TestDependencySentinelYarnDeny:
    """yarn add for denied npm packages should also be blocked."""

    def test_yarn_add_typosquat(self, runner):
        result = runner.run(make_bash_input("yarn add crossenv"))
        assert result.is_deny

    def test_yarn_add_safe(self, runner):
        result = runner.run(make_bash_input("yarn add lodash"))
        assert result.is_allow


# ── Non-install commands (ALLOW) ────────────────────────────────────────────

class TestDependencySentinelNonInstall:
    """Commands that aren't package installs should pass through."""

    def test_pip_list(self, runner):
        result = runner.run(make_bash_input("pip list"))
        assert result.is_allow

    def test_pip_freeze(self, runner):
        result = runner.run(make_bash_input("pip freeze"))
        assert result.is_allow

    def test_npm_test(self, runner):
        result = runner.run(make_bash_input("npm test"))
        assert result.is_allow

    def test_non_package_command(self, runner):
        result = runner.run(make_bash_input("ls -la"))
        assert result.is_allow

    def test_python_script(self, runner):
        result = runner.run(make_bash_input("python3 app.py"))
        assert result.is_allow


# ── Non-Bash tool types (ALLOW) ────────────────────────────────────────────

class TestDependencySentinelNonBash:
    """Non-Bash tool types should pass through immediately."""

    def test_read_tool_passthrough(self, runner):
        result = runner.run({
            "tool_name": "Read",
            "tool_input": {"file_path": "setup.py"},
        })
        assert result.is_allow

    def test_write_tool_passthrough(self, runner):
        result = runner.run({
            "tool_name": "Write",
            "tool_input": {"file_path": "app.py"},
        })
        assert result.is_allow


# ── Exit code behavior ─────────────────────────────────────────────────────

class TestDependencySentinelExitCodes:
    """All exits should be 0 (deny via JSON, not exit code)."""

    def test_allow_exit_0(self, runner):
        result = runner.run(make_bash_input("pip install flask"))
        assert result.exit_code == 0

    def test_deny_exit_0(self, runner):
        result = runner.run(make_bash_input("pip install colourama"))
        assert result.exit_code == 0

    def test_deny_has_json_structure(self, runner):
        result = runner.run(make_bash_input("pip install colourama"))
        assert result.json_output is not None
        hso = result.json_output.get("hookSpecificOutput", {})
        assert hso.get("permissionDecision") == "deny"
        assert "Dependency Sentinel" in hso.get("permissionDecisionReason", "")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
