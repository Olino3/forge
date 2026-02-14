"""Test Forge coding conventions from forge-convention-enforcer workflow.

Validates:
1. Kebab-case naming for skill directories, agents, context, commands
2. Agent file pairing ({name}.md + {name}.config.json)
3. Context frontmatter presence
4. Hook scripts include `set -euo pipefail`
5. ATX heading consistency in markdown files

Migrated from .github/workflows/forge-convention-enforcer.md as part of Phase 2 optimization.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR, extract_yaml_frontmatter


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KEBAB_CASE_PATTERN = re.compile(r'^[a-z]+(-[a-z]+)*$')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_kebab_case(name: str) -> bool:
    """Check if name follows kebab-case convention."""
    return bool(KEBAB_CASE_PATTERN.match(name))


def _get_skill_directories() -> list[tuple[str, Path]]:
    """Return (skill_name, skill_dir) for all skill directories."""
    skills_dir = FORGE_DIR / "skills"
    skill_dirs = [
        d for d in sorted(skills_dir.iterdir())
        if d.is_dir() and d.name not in ["__pycache__"]
    ]
    return [(d.name, d) for d in skill_dirs]


def _get_agent_files() -> list[tuple[str, Path]]:
    """Return (agent_name, config_path) for all agent configs."""
    agents_dir = FORGE_DIR / "agents"
    configs = sorted(agents_dir.glob("*.config.json"))
    return [(p.stem, p) for p in configs]


def _get_command_files() -> list[tuple[str, Path]]:
    """Return (command_name, command_path) for all command .md files."""
    commands_dir = FORGE_DIR / "commands"
    commands = [
        f for f in sorted(commands_dir.glob("*.md"))
        if f.name not in ["index.md"]
    ]
    return [(f.stem, f) for f in commands]


def _get_context_files() -> list[tuple[str, Path]]:
    """Return (filename, path) for all context .md files."""
    context_dir = FORGE_DIR / "context"
    files = []
    
    for domain_dir in sorted(context_dir.iterdir()):
        if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
            for md_file in sorted(domain_dir.rglob("*.md")):
                if md_file.name not in ["index.md"]:
                    files.append((md_file.stem, md_file))
    
    return files


def _get_hook_scripts() -> list[tuple[str, Path]]:
    """Return (hook_name, hook_path) for all hook .sh files."""
    hooks_dir = FORGE_DIR / "hooks"
    hooks = sorted(hooks_dir.glob("*.sh"))
    return [(h.stem, h) for h in hooks]


def _get_markdown_files() -> list[tuple[str, Path]]:
    """Get all markdown files in forge-plugin/."""
    md_files = []
    for md_path in sorted(FORGE_DIR.rglob("*.md")):
        # Skip vendor directories and caches
        if any(part.startswith('.') or part == '__pycache__' for part in md_path.parts):
            continue
        rel_path = md_path.relative_to(FORGE_DIR)
        md_files.append((str(rel_path), md_path))
    return md_files


# ---------------------------------------------------------------------------
# Test Classes
# ---------------------------------------------------------------------------

class TestNamingConventions:
    """Check 1: Validate kebab-case naming conventions."""

    @pytest.mark.parametrize(
        "skill_name,skill_dir",
        _get_skill_directories(),
        ids=[name for name, _ in _get_skill_directories()],
    )
    def test_skill_directories_kebab_case(self, skill_name, skill_dir):
        """Skill directory names must use kebab-case."""
        assert _is_kebab_case(skill_name), (
            f"Skill directory '{skill_name}' does not follow kebab-case convention. "
            f"Expected format: lowercase-with-hyphens"
        )

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_files(),
        ids=[name for name, _ in _get_agent_files()],
    )
    def test_agent_names_kebab_case(self, agent_name, config_path):
        """Agent file names must use kebab-case."""
        assert _is_kebab_case(agent_name), (
            f"Agent '{agent_name}' does not follow kebab-case convention"
        )

    @pytest.mark.parametrize(
        "command_name,command_path",
        _get_command_files(),
        ids=[name for name, _ in _get_command_files()],
    )
    def test_command_names_kebab_case(self, command_name, command_path):
        """Command file names must use kebab-case."""
        assert _is_kebab_case(command_name), (
            f"Command '{command_name}' does not follow kebab-case convention"
        )

    @pytest.mark.parametrize(
        "context_name,context_path",
        _get_context_files(),
        ids=[name for name, _ in _get_context_files()],
    )
    def test_context_file_names_kebab_case(self, context_name, context_path):
        """Context file names should use kebab-case."""
        # Some exceptions allowed for special files
        exceptions = ["README", "SKILL_TEMPLATE", "OUTPUT_CONVENTIONS"]
        
        if context_name.upper() in exceptions:
            pytest.skip(f"'{context_name}' is an allowed exception")
        
        # Allow underscore-separated names for some legacy files
        if '_' in context_name:
            pytest.skip(f"'{context_name}' uses underscore separation (legacy)")
        
        assert _is_kebab_case(context_name), (
            f"Context file '{context_name}' should follow kebab-case convention"
        )


class TestAgentFilePairing:
    """Check 2: Validate agent file pairing."""

    @pytest.mark.parametrize(
        "agent_name,config_path",
        _get_agent_files(),
        ids=[name for name, _ in _get_agent_files()],
    )
    def test_agent_has_both_md_and_config(self, agent_name, config_path):
        """Each agent must have both {name}.md and {name}.config.json."""
        md_path = config_path.with_suffix('.md')
        
        assert md_path.exists(), (
            f"Agent '{agent_name}' has config file but missing personality file: "
            f"{md_path.name}"
        )

    def test_no_orphaned_agent_md_files(self):
        """No .md files in agents/ without corresponding .config.json."""
        agents_dir = FORGE_DIR / "agents"
        md_files = sorted(agents_dir.glob("*.md"))
        
        orphaned = []
        for md_file in md_files:
            config_file = md_file.with_suffix('.config.json')
            if not config_file.exists():
                orphaned.append(md_file.name)
        
        assert not orphaned, (
            f"Found agent personality files without corresponding config files:\n  " +
            "\n  ".join(orphaned)
        )


class TestContextFrontmatter:
    """Check 3: Context frontmatter presence."""

    @pytest.mark.parametrize(
        "context_name,context_path",
        _get_context_files(),
        ids=[name for name, _ in _get_context_files()],
    )
    def test_context_has_frontmatter(self, context_name, context_path):
        """All context files should have YAML frontmatter."""
        frontmatter = extract_yaml_frontmatter(context_path)
        
        assert frontmatter is not None, (
            f"Context file '{context_path.relative_to(FORGE_DIR)}' missing YAML frontmatter"
        )


class TestHookScriptStandards:
    """Check 4: Hook script standards."""

    @pytest.mark.parametrize(
        "hook_name,hook_path",
        _get_hook_scripts(),
        ids=[name for name, _ in _get_hook_scripts()],
    )
    def test_hook_has_set_euo_pipefail(self, hook_name, hook_path):
        """Hook scripts must include `set -euo pipefail`."""
        content = hook_path.read_text(encoding='utf-8')
        
        # Check for set -euo pipefail or set -e -u -o pipefail
        has_set_e = re.search(r'set\s+-[euo]+', content)
        has_pipefail = 'pipefail' in content
        
        assert has_set_e and has_pipefail, (
            f"Hook '{hook_name}' missing 'set -euo pipefail' at the start. "
            f"This ensures the script fails fast on errors."
        )

    @pytest.mark.parametrize(
        "hook_name,hook_path",
        _get_hook_scripts(),
        ids=[name for name, _ in _get_hook_scripts()],
    )
    def test_hook_no_destructive_patterns(self, hook_name, hook_path):
        """Hook scripts should avoid unsafe/destructive command patterns."""
        content = hook_path.read_text(encoding='utf-8')
        
        # Patterns that are potentially destructive
        unsafe_patterns = [
            (r'rm\s+-rf\s+/', "rm -rf / (recursive delete from root)"),
            (r':\s*>\s*[^>]', ": > file (file truncation without safeguards)"),
            (r'dd\s+if=.*of=/dev/', "dd to block device"),
        ]
        
        violations = []
        for pattern, description in unsafe_patterns:
            if re.search(pattern, content):
                violations.append(description)
        
        assert not violations, (
            f"Hook '{hook_name}' contains potentially unsafe patterns:\n  " +
            "\n  ".join(violations)
        )


class TestMarkdownConventions:
    """Check 5: ATX heading consistency."""

    @pytest.mark.parametrize(
        "rel_path,md_path",
        _get_markdown_files(),
        ids=[rel_path for rel_path, _ in _get_markdown_files()],
    )
    def test_markdown_uses_atx_headings(self, rel_path, md_path):
        """Markdown files should use ATX-style headings (# ## ###) not Setext (=== ---)."""
        content = md_path.read_text(encoding='utf-8')
        
        # Check for Setext-style headings (underlined with = or -)
        # Match lines that are all === or all ---
        setext_pattern = re.compile(r'^\s*[=\-]{3,}\s*$', re.MULTILINE)
        setext_matches = setext_pattern.findall(content)
        
        if setext_matches:
            pytest.fail(
                f"File '{rel_path}' uses Setext-style headings (underlined with === or ---). "
                f"Prefer ATX-style headings (# ## ###) for consistency."
            )
