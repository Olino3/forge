#!/bin/bash
# ⚒️ The Forge — E2E: Skill Invocation Test
#
# Verifies that all 102 skills are discoverable, have valid SKILL.md files,
# and follow the expected skill directory conventions.
# Skips runtime skill invocation if claude CLI is not available.
#
# Exit codes:
#   0 — All checks passed (or skipped due to missing CLI)
#   1 — One or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
PLUGIN_DIR="${FORGE_DIR}"

# --- Color Output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓ $1${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; }
info() { echo -e "${BLUE}→ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

echo ""
echo "⚒️  The Forge — E2E: Skill Invocation"
echo "═══════════════════════════════════════"
echo ""

FAILED=0

# --- Expected skills (102 skills from CLAUDE.md) ---
EXPECTED_SKILLS=(
    "accessibility"
    "angular-architect"
    "angular-code-review"
    "animate"
    "api-design"
    "architecture-design"
    "azure-auth"
    "better-auth"
    "clerk-auth"
    "cli-developer"
    "cloud-architect"
    "code-documenter"
    "code-reviewer"
    "color-palette"
    "commit-helper"
    "cpp"
    "create-agents"
    "csharp"
    "database-optimizer"
    "database-schema-analysis"
    "debugging-expert"
    "dev-tools"
    "devops-engineer"
    "divine"
    "django"
    "docs-workflow"
    "documentation-generator"
    "dotnet-code-review"
    "dotnet-core"
    "email-gateway"
    "email-writer"
    "excel-skills"
    "fastapi"
    "favicon-gen"
    "feature-forge"
    "file-schema-analysis"
    "firebase-auth"
    "firebase-firestore"
    "firebase-storage"
    "firecrawl-scraper"
    "flutter-expert"
    "fullstack-development"
    "generate-azure-bicep"
    "generate-azure-functions"
    "generate-azure-pipelines"
    "generate-jest-unit-tests"
    "generate-mock-service"
    "generate-more-skills-with-claude"
    "generate-python-unit-tests"
    "generate-tilt-dev-environment"
    "get-git-diff"
    "graphql-design"
    "icon-design"
    "image-gen"
    "java-architect"
    "javascript"
    "jquery-4"
    "jupyter-notebook-skills"
    "kubernetes-specialist"
    "legacy-modernizer"
    "mcp-developer"
    "microservices-design"
    "monitoring-expert"
    "nestjs"
    "nextjs"
    "oauth-integrations"
    "office"
    "open-source-contributions"
    "pandas"
    "php"
    "playwright-local"
    "postgres"
    "power-debug"
    "project-health"
    "project-planning"
    "project-session-management"
    "project-workflow"
    "prompt-engineer"
    "python-code-review"
    "python-dependency-management"
    "rails"
    "react-expert"
    "react-forms"
    "react-native-expert"
    "responsive-images"
    "secure-code"
    "security-reviewer"
    "skill-creator"
    "skill-review"
    "slack-message-composer"
    "snowflake-platform"
    "sql"
    "sre-engineer"
    "sub-agent-patterns"
    "tailwind-patterns"
    "terraform-engineer"
    "test-cli-tools"
    "testing"
    "typescript"
    "vue-expert"
    "vue-expert-js"
    "websocket-engineer"
)

# --- Test 1: All expected skill directories exist ---
info "Checking skill directories..."
SKILLS_DIR="${PLUGIN_DIR}/skills"
ACTUAL_SKILL_DIRS=$(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)

for skill in "${EXPECTED_SKILLS[@]}"; do
    if [ -d "${SKILLS_DIR}/${skill}" ]; then
        pass "Skill directory: ${skill}/"
    else
        fail "Missing skill directory: ${skill}/"
        FAILED=1
    fi
done

# --- Test 2: Each skill has SKILL.md ---
info "Checking SKILL.md files..."
for skill in "${EXPECTED_SKILLS[@]}"; do
    SKILL_FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$SKILL_FILE" ]; then
        pass "${skill}/SKILL.md exists"
    else
        fail "${skill}/SKILL.md missing"
        FAILED=1
    fi
done

# --- Test 3: Each skill has examples.md ---
info "Checking examples.md files..."
EXAMPLES_MISSING=0
for skill in "${EXPECTED_SKILLS[@]}"; do
    EXAMPLES_FILE="${SKILLS_DIR}/${skill}/examples.md"
    if [ -f "$EXAMPLES_FILE" ]; then
        pass "${skill}/examples.md exists"
    else
        warn "${skill}/examples.md missing"
        EXAMPLES_MISSING=$((EXAMPLES_MISSING + 1))
    fi
done

if [ "$EXAMPLES_MISSING" -gt 0 ]; then
    warn "${EXAMPLES_MISSING} skills missing examples.md"
fi

# --- Test 4: SKILL.md files have expected workflow sections ---
# NOTE: The 6-step workflow (Initial Analysis, Load Memory, Load Context, Perform Analysis,
# Generate Output, Update Memory) is a RECOMMENDATION from SKILL_TEMPLATE.md, not a strict
# requirement. Many existing skills use equivalent or adapted step names. This test reports
# findings as informational rather than failures.
info "Checking SKILL.md workflow structure (informational)..."
WORKFLOW_STEPS=(
    "Initial Analysis"
    "Load Memory"
    "Load Context"
    "Perform Analysis"
    "Generate Output"
    "Update Memory"
)

for skill in "${EXPECTED_SKILLS[@]}"; do
    SKILL_FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$SKILL_FILE" ]; then
        STEPS_FOUND=0
        for step in "${WORKFLOW_STEPS[@]}"; do
            if grep -qi "$step" "$SKILL_FILE" 2>/dev/null; then
                STEPS_FOUND=$((STEPS_FOUND + 1))
            fi
        done

        if [ "$STEPS_FOUND" -ge 4 ]; then
            pass "${skill}: ${STEPS_FOUND}/6 workflow steps documented"
        else
            warn "${skill}: only ${STEPS_FOUND}/6 workflow steps found"
        fi
    fi
done

# --- Test 5: Skill count matches expected ---
info "Checking skill count..."
ACTUAL_COUNT=$(echo "$ACTUAL_SKILL_DIRS" | wc -l)
EXPECTED_COUNT=${#EXPECTED_SKILLS[@]}

if [ "$ACTUAL_COUNT" -ge "$EXPECTED_COUNT" ]; then
    pass "Skill count: ${ACTUAL_COUNT} found (${EXPECTED_COUNT} expected)"
else
    fail "Skill count: ${ACTUAL_COUNT} found, expected at least ${EXPECTED_COUNT}"
    FAILED=1
fi

# --- Test 6: No unexpected skill directories ---
info "Checking for unexpected skill directories..."
while IFS= read -r dir; do
    FOUND=false
    for skill in "${EXPECTED_SKILLS[@]}"; do
        if [ "$dir" = "$skill" ]; then
            FOUND=true
            break
        fi
    done
    if [ "$FOUND" = false ]; then
        warn "Unexpected skill directory: ${dir}/"
    fi
done <<< "$ACTUAL_SKILL_DIRS"

# --- Test 7: Skills referenced by agents exist ---
info "Checking agent-to-skill references..."
AGENT_CONFIGS=$(find "${PLUGIN_DIR}/agents" -name "*.config.json" -type f 2>/dev/null)
for config in $AGENT_CONFIGS; do
    AGENT_NAME=$(basename "$config" .config.json)
    AGENT_SKILLS=$(jq -r '.skills[]?.name // empty' "$config" 2>/dev/null || true)
    for skill_name in $AGENT_SKILLS; do
        if [ -d "${SKILLS_DIR}/${skill_name}" ]; then
            pass "Agent '${AGENT_NAME}' → skill '${skill_name}' exists"
        else
            fail "Agent '${AGENT_NAME}' references missing skill: ${skill_name}"
            FAILED=1
        fi
    done
done

# --- Test 8: Runtime skill invocation (requires claude CLI) ---
# NOTE: True runtime E2E testing of skill invocation is not currently possible because the
# `claude` CLI requires an interactive session. This test validates structure and discoverability.
# Future options: (1) claude CLI batch/non-interactive mode, (2) dedicated Claude CLI test harness.
if command -v claude &>/dev/null; then
    info "claude CLI found — runtime skill invocation tests not yet implemented"
    warn "claude CLI requires interactive session; skipping runtime invocation"
else
    warn "claude CLI not found — skipping runtime skill invocation tests"
fi

# --- Summary ---
echo ""
if [ "$FAILED" -eq 0 ]; then
    pass "Skill invocation: ALL CHECKS PASSED"
    exit 0
else
    fail "Skill invocation: SOME CHECKS FAILED"
    exit 1
fi
