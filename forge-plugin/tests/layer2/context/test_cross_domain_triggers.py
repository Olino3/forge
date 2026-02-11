"""Tests for cross-domain trigger validation — independent of hooks.

Validates the cross-domain trigger matrix from cross_domain.md:
  1. All crossDomainTriggers in agent configs target existing files
  2. No self-referential triggers (a domain triggering itself)
  3. Trigger format matches domain/filename pattern
  4. No circular trigger chains (A→B→A)

Also validates the cross_domain.md matrix entries themselves:
  - Referenced secondary context files exist
  - Format is consistent
"""

import re
from pathlib import Path

import pytest
import yaml

from conftest import FORGE_DIR, extract_yaml_frontmatter, load_json


CONTEXT_DIR = FORGE_DIR / "context"
AGENTS_DIR = FORGE_DIR / "agents"

KNOWN_DOMAINS = [
    "angular",
    "azure",
    "commands",
    "dotnet",
    "engineering",
    "git",
    "python",
    "schema",
    "security",
]

# Pattern for cross-domain trigger references: domain/filename
TRIGGER_PATTERN = re.compile(r"^[a-z]+/[a-z_]+$")


def _get_agent_configs() -> list[tuple[str, dict]]:
    """Return (name, config) for all agent config.json files."""
    configs = []
    for cfg_file in AGENTS_DIR.glob("*.config.json"):
        try:
            config = load_json(cfg_file)
            configs.append((cfg_file.stem.replace(".config", ""), config))
        except Exception:
            continue
    return configs


def _collect_cross_domain_triggers() -> list[tuple[str, str]]:
    """Collect all (agent_name, trigger) pairs from agent configs."""
    triggers = []
    for name, config in _get_agent_configs():
        context = config.get("context", {})
        cdt = context.get("crossDomainTriggers", [])
        for trigger in cdt:
            if isinstance(trigger, str):
                triggers.append((name, trigger))
            elif isinstance(trigger, dict):
                # Some configs may use dict format with 'target' key
                target = trigger.get("target", trigger.get("file", ""))
                if target:
                    triggers.append((name, target))
    return triggers


# ── Cross-domain trigger format ──────────────────────────────────────

class TestTriggerFormat:
    """Trigger references should match the domain/filename pattern."""

    def test_all_triggers_match_pattern(self):
        """Every crossDomainTrigger should match 'domain/filename' format."""
        invalid = []
        for agent, trigger in _collect_cross_domain_triggers():
            if not TRIGGER_PATTERN.match(trigger):
                invalid.append(f"Agent '{agent}': trigger '{trigger}'")
        if not _collect_cross_domain_triggers():
            pytest.skip("No cross-domain triggers found in agent configs")
        assert not invalid, (
            f"Triggers with invalid format (expected 'domain/filename'):\n"
            + "\n".join(f"  - {i}" for i in invalid)
        )


# ── Trigger targets exist ────────────────────────────────────────────

class TestTriggerTargetsExist:
    """All cross-domain trigger targets should reference existing files."""

    def test_all_trigger_files_exist(self):
        """Every crossDomainTrigger target should resolve to an existing file."""
        missing = []
        for agent, trigger in _collect_cross_domain_triggers():
            # Trigger format: domain/filename → context/{domain}/{filename}.md
            parts = trigger.split("/")
            if len(parts) == 2:
                domain, filename = parts
                target_path = CONTEXT_DIR / domain / f"{filename}.md"
                if not target_path.exists():
                    missing.append(
                        f"Agent '{agent}': {trigger} → {target_path.relative_to(FORGE_DIR)}"
                    )
        if not _collect_cross_domain_triggers():
            pytest.skip("No cross-domain triggers found in agent configs")
        assert not missing, (
            f"Triggers referencing non-existent files:\n"
            + "\n".join(f"  - {m}" for m in missing)
        )


# ── No self-referential triggers ─────────────────────────────────────

class TestNoSelfReferentialTriggers:
    """A domain should not trigger itself (would be a loading loop)."""

    def test_no_self_referencing(self):
        """Agent's primary domain should not appear in its own crossDomainTriggers."""
        self_refs = []
        for name, config in _get_agent_configs():
            context = config.get("context", {})
            primary_domains = context.get("primaryDomains", [])
            cdt = context.get("crossDomainTriggers", [])

            for trigger in cdt:
                trigger_str = trigger if isinstance(trigger, str) else trigger.get("target", "")
                parts = trigger_str.split("/")
                if len(parts) >= 1:
                    trigger_domain = parts[0]
                    if trigger_domain in primary_domains:
                        self_refs.append(
                            f"Agent '{name}': primary domain '{trigger_domain}' "
                            f"in crossDomainTrigger '{trigger_str}'"
                        )
        if not self_refs:
            return  # No self-refs found — pass
        assert not self_refs, (
            f"Self-referential cross-domain triggers found:\n"
            + "\n".join(f"  - {s}" for s in self_refs)
        )


# ── No circular trigger chains ───────────────────────────────────────

class TestNoCircularTriggers:
    """Cross-domain triggers should not form circular chains."""

    def test_no_simple_cycles(self):
        """Check for A→B→A circular references between domains.

        Build a graph of domain→triggered_domain edges from agent configs,
        then check for any 2-step cycles (A→B→A).
        """
        # Build adjacency map: domain → set of triggered domains
        domain_triggers: dict[str, set[str]] = {}

        for name, config in _get_agent_configs():
            context = config.get("context", {})
            primary_domains = context.get("primaryDomains", [])
            cdt = context.get("crossDomainTriggers", [])

            for pd in primary_domains:
                if pd not in domain_triggers:
                    domain_triggers[pd] = set()

            for trigger in cdt:
                trigger_str = trigger if isinstance(trigger, str) else trigger.get("target", "")
                parts = trigger_str.split("/")
                if len(parts) >= 1:
                    triggered_domain = parts[0]
                    for pd in primary_domains:
                        domain_triggers.setdefault(pd, set()).add(triggered_domain)

        # Check for 2-cycle: A triggers B and B triggers A
        cycles = []
        for domain_a, targets_a in domain_triggers.items():
            for domain_b in targets_a:
                targets_b = domain_triggers.get(domain_b, set())
                if domain_a in targets_b:
                    cycle = tuple(sorted([domain_a, domain_b]))
                    if cycle not in cycles:
                        cycles.append(cycle)

        assert not cycles, (
            f"Circular cross-domain trigger chains detected:\n"
            + "\n".join(f"  - {a} ↔ {b}" for a, b in cycles)
        )


# ── cross_domain.md matrix entries ───────────────────────────────────

class TestCrossDomainMatrixFile:
    """Validate the cross_domain.md file itself."""

    def test_cross_domain_file_exists(self):
        assert (CONTEXT_DIR / "cross_domain.md").exists()

    def test_cross_domain_has_frontmatter(self):
        fm = extract_yaml_frontmatter(CONTEXT_DIR / "cross_domain.md")
        assert fm is not None

    def test_referenced_security_guidelines_exists(self):
        """security/security_guidelines.md is heavily referenced and must exist."""
        path = CONTEXT_DIR / "security" / "security_guidelines.md"
        assert path.exists(), (
            f"security/security_guidelines.md referenced in cross_domain.md "
            f"but not found at {path}"
        )

    def test_referenced_common_patterns_exists(self):
        """schema/common_patterns.md is referenced and must exist."""
        path = CONTEXT_DIR / "schema" / "common_patterns.md"
        assert path.exists(), (
            f"schema/common_patterns.md referenced in cross_domain.md "
            f"but not found at {path}"
        )

    def test_cross_domain_matrix_content(self):
        """cross_domain.md should contain a trigger matrix table."""
        content = (CONTEXT_DIR / "cross_domain.md").read_text()
        assert "Trigger" in content or "trigger" in content
        assert "|" in content  # Should have a markdown table


# ── Domain trigger targets from index files ──────────────────────────

class TestIndexCrossDomainTriggers:
    """Index files may reference cross-domain triggers; verify those targets."""

    @pytest.mark.parametrize("domain", KNOWN_DOMAINS)
    def test_index_cross_domain_references(self, domain):
        """Any crossDomainTriggers in {domain}/index.md should target existing files."""
        index_path = CONTEXT_DIR / domain / "index.md"
        if not index_path.exists():
            pytest.skip(f"No index.md for {domain}")
        fm = extract_yaml_frontmatter(index_path)
        if fm is None:
            pytest.skip(f"No frontmatter in {domain}/index.md")

        triggers = fm.get("crossDomainTriggers", [])
        if not triggers:
            pytest.skip(f"No crossDomainTriggers in {domain}/index.md")

        missing = []
        for trigger in triggers:
            trigger_str = trigger if isinstance(trigger, str) else trigger.get("target", "")
            parts = trigger_str.split("/")
            if len(parts) == 2:
                target_domain, target_file = parts
                target_path = CONTEXT_DIR / target_domain / f"{target_file}.md"
                if not target_path.exists():
                    missing.append(f"{trigger_str} → {target_path.relative_to(FORGE_DIR)}")

        assert not missing, (
            f"{domain}/index.md has cross-domain triggers to non-existent files:\n"
            + "\n".join(f"  - {m}" for m in missing)
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
