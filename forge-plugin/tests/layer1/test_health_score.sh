#!/usr/bin/env bash
# Test health score aggregator from forge-health-dashboard workflow
#
# Aggregates:
# 1. Component counts (skills, agents, hooks, context files, commands)
# 2. Cross-reference tallies from other validation jobs
# 3. File existence and structural health
# 4. Generate JSON health report artifact
#
# Migrated from .github/workflows/forge-health-dashboard.md as part of Phase 2 optimization

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="${SCRIPT_DIR}/../.."
REPO_ROOT="${FORGE_DIR}/.."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "📊 Generating Forge Health Report..."
echo

# ---------------------------------------------------------------------------
# Section 1: Component Counts
# ---------------------------------------------------------------------------

echo "Section 1: Counting components..."

skill_count=$(find "${FORGE_DIR}/skills" -mindepth 1 -maxdepth 1 -type d ! -name '__pycache__' | wc -l)
agent_count=$(find "${FORGE_DIR}/agents" -name '*.config.json' | wc -l)
hook_count=$(find "${FORGE_DIR}/hooks" -name '*.sh' | wc -l)
command_count=$(find "${FORGE_DIR}/commands" -name '*.md' ! -name 'index.md' | wc -l)

# Context file count (all .md files in domain directories, excluding index.md)
context_count=0
for domain in engineering angular azure commands dotnet git python schema security; do
    if [[ -d "${FORGE_DIR}/context/${domain}" ]]; then
        domain_files=$(find "${FORGE_DIR}/context/${domain}" -name '*.md' ! -name 'index.md' | wc -l)
        context_count=$((context_count + domain_files))
    fi
done

echo "  Skills: $skill_count"
echo "  Agents: $agent_count"
echo "  Hooks: $hook_count"
echo "  Commands: $command_count"
echo "  Context files: $context_count"
echo

# ---------------------------------------------------------------------------
# Section 2: File Existence Checks
# ---------------------------------------------------------------------------

echo "Section 2: Critical file existence..."

critical_files=(
    "forge-plugin/interfaces/schemas/agent_config.schema.json"
    "forge-plugin/hooks/hooks.json"
    "forge-plugin/hooks/HOOKS_GUIDE.md"
    "forge-plugin/context/index.md"
    "forge-plugin/context/loading_protocol.md"
    "forge-plugin/memory/lifecycle.md"
    "forge-plugin/skills/SKILL_TEMPLATE.md"
    ".github/workflows/forge-tests.yml"
)

missing_count=0
for file in "${critical_files[@]}"; do
    if [[ ! -f "${REPO_ROOT}/${file}" ]]; then
        echo "${YELLOW}  ⚠️  Missing: $file${NC}"
        missing_count=$((missing_count + 1))
    fi
done

if [[ $missing_count -eq 0 ]]; then
    echo "${GREEN}  ✅ All critical files present${NC}"
else
    echo "${YELLOW}  ⚠️  $missing_count critical files missing${NC}"
fi
echo

# ---------------------------------------------------------------------------
# Section 3: Cross-Reference Tallies
# ---------------------------------------------------------------------------

echo "Section 3: Cross-reference health..."

# Count agent-skill references
agent_skill_refs=0
if command -v jq &>/dev/null; then
    for agent_config in "${FORGE_DIR}/agents"/*.config.json; do
        [[ -f "$agent_config" ]] || continue
        refs=$(jq -r '.skills[]?.name // empty' "$agent_config" 2>/dev/null | wc -l)
        agent_skill_refs=$((agent_skill_refs + refs))
    done
    echo "  Agent → Skill references: $agent_skill_refs"
fi

# Count domain directories with index files
indexed_domains=0
for domain in engineering angular azure commands dotnet git python schema security; do
    if [[ -f "${FORGE_DIR}/context/${domain}/index.md" ]]; then
        indexed_domains=$((indexed_domains + 1))
    fi
done
echo "  Indexed context domains: $indexed_domains"

# Count hook registrations
if [[ -f "${FORGE_DIR}/hooks/hooks.json" ]] && command -v jq &>/dev/null; then
    hook_registrations=$(jq '[.events[]?.handlers[]?] | length' "${FORGE_DIR}/hooks/hooks.json" 2>/dev/null || echo 0)
    echo "  Hook registrations: $hook_registrations"
fi

echo

# ---------------------------------------------------------------------------
# Section 4: MCP Integration
# ---------------------------------------------------------------------------

echo "Section 4: MCP integration..."

mcp_count=$(find "${FORGE_DIR}/mcps" -name '*.md' ! -name 'index.md' 2>/dev/null | wc -l || echo 0)
echo "  MCP documentation files: $mcp_count"

# Count external plugin integrations
external_plugins=0
if [[ -f "${REPO_ROOT}/.claude-plugin/marketplace.json" ]] && command -v jq &>/dev/null; then
    external_plugins=$(jq -r '.plugins | length' "${REPO_ROOT}/.claude-plugin/marketplace.json" 2>/dev/null || echo 0)
    echo "  External plugin integrations: $external_plugins"
fi

echo

# ---------------------------------------------------------------------------
# Section 5: Generate JSON Report
# ---------------------------------------------------------------------------

echo "Section 5: Generating JSON report..."

report_file="${FORGE_DIR}/tests/.health-report.json"

# Build JSON report (compatible with basic bash - no jq required for generation)
cat > "$report_file" <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "components": {
    "skills": ${skill_count},
    "agents": ${agent_count},
    "hooks": ${hook_count},
    "commands": ${command_count},
    "context_files": ${context_count}
  },
  "critical_files": {
    "total": ${#critical_files[@]},
    "missing": ${missing_count}
  },
  "cross_references": {
    "agent_skill_refs": ${agent_skill_refs},
    "indexed_domains": ${indexed_domains}
  },
  "integrations": {
    "mcp_docs": ${mcp_count},
    "external_plugins": ${external_plugins}
  },
  "health_status": "$([[ $missing_count -eq 0 ]] && echo "healthy" || echo "degraded")"
}
EOF

echo "${GREEN}  ✅ Health report written to: ${report_file}${NC}"
echo

# ---------------------------------------------------------------------------
# Section 6: Summary Output
# ---------------------------------------------------------------------------

echo "${CYAN}═══════════════════════════════════════${NC}"
echo "${CYAN}  Forge Health Summary${NC}"
echo "${CYAN}═══════════════════════════════════════${NC}"
echo "  Total Components: $((skill_count + agent_count + hook_count + command_count + context_count))"
echo "  Agent → Skill refs: $agent_skill_refs"
echo "  Critical files: ${#critical_files[@]} total, $missing_count missing"
echo "  Status: $([[ $missing_count -eq 0 ]] && echo "${GREEN}HEALTHY${NC}" || echo "${YELLOW}DEGRADED${NC}")"
echo "${CYAN}═══════════════════════════════════════${NC}"
echo

if command -v jq &>/dev/null; then
    echo "JSON Report:"
    jq '.' "$report_file"
fi

exit 0
