#!/bin/bash
# pii_redactor.sh — The Shield: Data Privacy Guard
#
# Hook:    UserPromptSubmit (no matcher — fires on every prompt)
# Layer:   §6.1 The Shield
# Purpose: Scan user prompts for potential PII (Personally Identifiable
#          Information) before the text enters the model's context.
#          Warns the user when PII patterns are detected.
#
# Detected patterns:
#   - Email addresses
#   - IP addresses (IPv4)
#   - Phone numbers (US/international formats)
#   - Social Security Numbers (SSN)
#   - Credit card numbers (Luhn-plausible 13-19 digit sequences)
#   - AWS access key IDs
#   - GitHub personal access tokens
#
# Behavior:
#   - Detection is best-effort via regex (some false positives expected)
#   - Outputs additionalContext warning to Claude on exit 0
#   - Does NOT block the prompt — warns only (user may intentionally include PII)
#   - Logs detections to the health buffer
#
# Input:  JSON on stdin (Claude Code UserPromptSubmit format)
# Output: JSON with additionalContext (warning) or silent exit 0

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)

# No prompt = nothing to scan
[[ -z "$PROMPT" ]] && exit 0

# --- PII pattern detection -----------------------------------------------
DETECTIONS=""
DETECTION_COUNT=0

# Email addresses
EMAIL_MATCHES=$(echo "$PROMPT" | grep -oEi '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' 2>/dev/null | head -5 || true)
if [[ -n "$EMAIL_MATCHES" ]]; then
    COUNT=$(echo "$EMAIL_MATCHES" | wc -l)
    DETECTIONS="${DETECTIONS}\n  - ${COUNT} email address(es) detected"
    DETECTION_COUNT=$((DETECTION_COUNT + COUNT))
fi

# IPv4 addresses (exclude common non-PII: 127.0.0.1, 0.0.0.0, 10.x, 192.168.x, 172.16-31.x)
IPV4_MATCHES=$(echo "$PROMPT" | grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' 2>/dev/null | \
    grep -vE '^(127\.0\.0\.1|0\.0\.0\.0|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|255\.)' 2>/dev/null | \
    head -5 || true)
if [[ -n "$IPV4_MATCHES" ]]; then
    COUNT=$(echo "$IPV4_MATCHES" | wc -l)
    DETECTIONS="${DETECTIONS}\n  - ${COUNT} public IP address(es) detected"
    DETECTION_COUNT=$((DETECTION_COUNT + COUNT))
fi

# US phone numbers (various formats)
PHONE_MATCHES=$(echo "$PROMPT" | grep -oE '(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b' 2>/dev/null | head -5 || true)
if [[ -n "$PHONE_MATCHES" ]]; then
    COUNT=$(echo "$PHONE_MATCHES" | wc -l)
    DETECTIONS="${DETECTIONS}\n  - ${COUNT} phone number(s) detected"
    DETECTION_COUNT=$((DETECTION_COUNT + COUNT))
fi

# Social Security Numbers (XXX-XX-XXXX or XXXXXXXXX)
SSN_MATCHES=$(echo "$PROMPT" | grep -oE '\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b' 2>/dev/null | head -5 || true)
if [[ -n "$SSN_MATCHES" ]]; then
    COUNT=$(echo "$SSN_MATCHES" | wc -l)
    DETECTIONS="${DETECTIONS}\n  - ${COUNT} possible SSN(s) detected"
    DETECTION_COUNT=$((DETECTION_COUNT + COUNT))
fi

# Credit card numbers (13-19 digits, optionally separated by spaces or dashes)
CC_MATCHES=$(echo "$PROMPT" | grep -oE '\b[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{1,7}\b' 2>/dev/null | head -5 || true)
if [[ -n "$CC_MATCHES" ]]; then
    COUNT=$(echo "$CC_MATCHES" | wc -l)
    DETECTIONS="${DETECTIONS}\n  - ${COUNT} possible credit card number(s) detected"
    DETECTION_COUNT=$((DETECTION_COUNT + COUNT))
fi

# AWS Access Key IDs
AWS_MATCHES=$(echo "$PROMPT" | grep -oE 'AKIA[0-9A-Z]{16}' 2>/dev/null | head -5 || true)
if [[ -n "$AWS_MATCHES" ]]; then
    COUNT=$(echo "$AWS_MATCHES" | wc -l)
    DETECTIONS="${DETECTIONS}\n  - ${COUNT} AWS access key(s) detected"
    DETECTION_COUNT=$((DETECTION_COUNT + COUNT))
fi

# GitHub tokens
GH_MATCHES=$(echo "$PROMPT" | grep -oE '(gh[ps]_[A-Za-z0-9_]{36,}|github_pat_[A-Za-z0-9_]{22,})' 2>/dev/null | head -5 || true)
if [[ -n "$GH_MATCHES" ]]; then
    COUNT=$(echo "$GH_MATCHES" | wc -l)
    DETECTIONS="${DETECTIONS}\n  - ${COUNT} GitHub token(s) detected"
    DETECTION_COUNT=$((DETECTION_COUNT + COUNT))
fi

# Private keys
if echo "$PROMPT" | grep -qE 'BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY' 2>/dev/null; then
    DETECTIONS="${DETECTIONS}\n  - Private key material detected"
    DETECTION_COUNT=$((DETECTION_COUNT + 1))
fi

# --- Output results ------------------------------------------------------
if [[ "$DETECTION_COUNT" -eq 0 ]]; then
    exit 0
fi

health_buffer_append "🛡️ PII redactor: ${DETECTION_COUNT} potential PII pattern(s) detected in user prompt"

# Build warning message
WARNING="⚠️ PII Detection Warning: ${DETECTION_COUNT} potential PII pattern(s) found in your prompt:"
WARNING="${WARNING}$(echo -e "$DETECTIONS")"
WARNING="${WARNING}"$'\n'"Consider removing personal data before it enters the AI context. This is a best-effort detection — some matches may be false positives."

# Escape for JSON
ESCAPED=$(echo "$WARNING" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')

cat <<EOF
{
  "additionalContext": "${ESCAPED}"
}
EOF
exit 0
