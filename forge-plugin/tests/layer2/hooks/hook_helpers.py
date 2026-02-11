"""Layer 2 Hook Testing Helpers.

Shared classes and constants for hook integration tests. Extracted from
conftest.py so test modules can import them without name-collisions with
the root-level tests/conftest.py.

Provides:
- HookResult: Structured result from running a hook script.
- HookRunner: Executes hook scripts via subprocess with JSON I/O.
- TempForgeEnvironment: Disposable .forge/ runtime directory for isolated tests.
- FORGE_DIR, REPO_ROOT, HOOKS_DIR: Resolved path constants.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path


# ── Resolve paths ──────────────────────────────────────────────────────────

def _resolve_forge_dir() -> Path:
    """Resolve the absolute path to the forge-plugin directory."""
    env_dir = os.environ.get("FORGE_DIR")
    if env_dir:
        p = Path(env_dir).resolve()
        if p.is_dir():
            return p

    current = Path(__file__).resolve().parent
    while current != current.parent:
        candidate = current / "forge-plugin"
        if candidate.is_dir():
            return candidate
        if current.name == "forge-plugin":
            return current
        current = current.parent

    return Path(__file__).resolve().parent.parent.parent


FORGE_DIR = _resolve_forge_dir()
REPO_ROOT = FORGE_DIR.parent
HOOKS_DIR = FORGE_DIR / "hooks"


# ── HookResult ─────────────────────────────────────────────────────────────

class HookResult:
    """Structured result from executing a hook script."""

    def __init__(self, exit_code: int, stdout: str, stderr: str):
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self._json_output: dict | None = None
        self._parsed = False

    @property
    def json_output(self) -> dict | None:
        """Parse stdout as JSON. Returns None if not valid JSON."""
        if not self._parsed:
            self._parsed = True
            stripped = self.stdout.strip()
            if stripped:
                try:
                    self._json_output = json.loads(stripped)
                except (json.JSONDecodeError, ValueError):
                    self._json_output = None
        return self._json_output

    @property
    def is_deny(self) -> bool:
        """True if hook output contains a deny decision."""
        j = self.json_output
        if not j:
            return False
        hso = j.get("hookSpecificOutput", {})
        return hso.get("permissionDecision") == "deny"

    @property
    def is_allow(self) -> bool:
        """True if hook did NOT output a deny decision.

        Hooks express "allow" by either:
        - Producing no JSON output (silent exit 0)
        - Producing JSON without a deny permissionDecision
        """
        return not self.is_deny

    @property
    def deny_reason(self) -> str:
        """The deny reason message, or empty string if not a deny."""
        if not self.is_deny:
            return ""
        j = self.json_output or {}
        hso = j.get("hookSpecificOutput", {})
        return hso.get("permissionDecisionReason", "")

    @property
    def additional_context(self) -> str:
        """The additionalContext warning, or empty string."""
        j = self.json_output
        if not j:
            return ""
        return j.get("additionalContext", "")

    @property
    def has_warning(self) -> bool:
        """True if hook output contains additionalContext (non-blocking warning)."""
        return bool(self.additional_context)

    def __repr__(self) -> str:
        status = "DENY" if self.is_deny else ("WARN" if self.has_warning else "ALLOW")
        return f"<HookResult exit={self.exit_code} {status}>"


# ── HookRunner ─────────────────────────────────────────────────────────────

class HookRunner:
    """Execute hook scripts via subprocess with JSON stdin.

    Usage::

        runner = HookRunner("sandbox_boundary_guard.sh")
        result = runner.run({"tool_name": "Read", "tool_input": {"file_path": "/etc/passwd"}})
        assert result.is_deny
    """

    def __init__(self, script_name: str, timeout: int = 10):
        self.script_path = HOOKS_DIR / script_name
        self.timeout = timeout

        if not self.script_path.exists():
            raise FileNotFoundError(f"Hook script not found: {self.script_path}")

    def run(
        self,
        input_json: dict | str,
        env_overrides: dict[str, str] | None = None,
        cwd: str | Path | None = None,
    ) -> HookResult:
        """Execute the hook script with JSON on stdin.

        Args:
            input_json: Dict (serialized to JSON) or raw JSON string to feed on stdin.
            env_overrides: Extra environment variables to set.
            cwd: Working directory for the subprocess (defaults to REPO_ROOT).

        Returns:
            HookResult with exit code, stdout, stderr, and parsed JSON.
        """
        if isinstance(input_json, dict):
            stdin_data = json.dumps(input_json)
        else:
            stdin_data = input_json

        # Build environment
        env = os.environ.copy()
        env["CLAUDE_PLUGIN_ROOT"] = str(FORGE_DIR)
        env["PATH"] = os.environ.get("PATH", "/usr/bin:/bin")
        if env_overrides:
            env.update(env_overrides)

        work_dir = str(cwd) if cwd else str(REPO_ROOT)

        try:
            proc = subprocess.run(
                ["bash", str(self.script_path)],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=work_dir,
                env=env,
            )
            return HookResult(proc.returncode, proc.stdout, proc.stderr)
        except subprocess.TimeoutExpired:
            return HookResult(-1, "", f"Hook timed out after {self.timeout}s")


# ── TempForgeEnvironment ───────────────────────────────────────────────────

class TempForgeEnvironment:
    """Disposable temporary directory structure mimicking .forge/ runtime state.

    Creates a temporary project directory with:
    - .forge/ runtime directory (health_buffer, etc.)
    - Optional .git/ directory for git-dependent hooks
    - Configurable staged files for pre-commit hooks

    Usage::

        with TempForgeEnvironment() as env:
            runner = HookRunner("sandbox_boundary_guard.sh")
            result = runner.run(input_json, cwd=env.project_root)
    """

    def __init__(self, init_git: bool = False):
        self._tmpdir: tempfile.TemporaryDirectory | None = None
        self._init_git = init_git
        self.project_root: Path = Path()
        self.forge_dir: Path = Path()

    def __enter__(self) -> "TempForgeEnvironment":
        self._tmpdir = tempfile.TemporaryDirectory(prefix="forge_test_")
        self.project_root = Path(self._tmpdir.name)
        self.forge_dir = self.project_root / ".forge"
        self.forge_dir.mkdir(parents=True)

        # Create health buffer files
        (self.forge_dir / "health_buffer").touch()
        (self.forge_dir / "health_buffer.lock").touch()

        if self._init_git:
            self._setup_git()

        return self

    def __exit__(self, *args):
        if self._tmpdir:
            self._tmpdir.cleanup()

    def _setup_git(self):
        """Initialize a minimal git repo in the project root."""
        subprocess.run(
            ["git", "init", "--initial-branch=develop"],
            cwd=str(self.project_root),
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@forge.dev"],
            cwd=str(self.project_root),
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Forge Test"],
            cwd=str(self.project_root),
            capture_output=True,
        )
        # Initial commit so HEAD exists
        (self.project_root / ".gitkeep").touch()
        subprocess.run(
            ["git", "add", "."],
            cwd=str(self.project_root),
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "chore: initial commit"],
            cwd=str(self.project_root),
            capture_output=True,
        )

    def create_file(self, relative_path: str, content: str = "") -> Path:
        """Create a file in the temp project directory."""
        fp = self.project_root / relative_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        return fp

    def stage_file(self, relative_path: str, content: str = ""):
        """Create a file and stage it in git (requires init_git=True)."""
        fp = self.create_file(relative_path, content)
        subprocess.run(
            ["git", "add", str(fp)],
            cwd=str(self.project_root),
            capture_output=True,
        )
        return fp

    @property
    def health_buffer_content(self) -> str:
        """Read the current health buffer contents."""
        hb = self.forge_dir / "health_buffer"
        if hb.exists():
            return hb.read_text(encoding="utf-8")
        return ""
