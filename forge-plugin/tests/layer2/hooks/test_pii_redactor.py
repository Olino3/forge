"""Tests for pii_redactor.sh — The Shield: Data Privacy Guard.

Validates that user prompts are scanned for PII patterns and appropriate
warnings are emitted. The PII redactor never blocks — it only warns via
additionalContext.

Event: UserPromptSubmit (no matcher — fires on every prompt)
"""

import pytest

from layer2.hooks.hook_helpers import HookRunner


SCRIPT = "pii_redactor.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


# ── Helpers ─────────────────────────────────────────────────────────────────

def make_prompt_input(prompt: str):
    return {"prompt": prompt}


# ── Clean prompts (no warning) ──────────────────────────────────────────────

class TestPiiCleanPrompts:
    """Clean prompts without PII should produce no output."""

    def test_normal_code_question(self, runner):
        result = runner.run(make_prompt_input(
            "Please help me refactor the UserService class to use dependency injection."
        ))
        assert result.is_allow
        assert not result.has_warning

    def test_empty_prompt(self, runner):
        result = runner.run(make_prompt_input(""))
        assert result.is_allow
        assert not result.has_warning

    def test_no_prompt_field(self, runner):
        result = runner.run({})
        assert result.is_allow
        assert not result.has_warning

    def test_code_with_numbers(self, runner):
        """Regular numbers in code context should not trigger."""
        result = runner.run(make_prompt_input(
            "The array has 1234 elements. Set timeout to 5000ms."
        ))
        assert result.is_allow
        assert not result.has_warning

    def test_private_ip_addresses(self, runner):
        """Private/local IPs (10.x, 192.168.x, 127.0.0.1) should not trigger."""
        result = runner.run(make_prompt_input(
            "Connect to 192.168.1.1 or 10.0.0.1 or 127.0.0.1 for testing."
        ))
        assert result.is_allow
        assert not result.has_warning


# ── Email detection ─────────────────────────────────────────────────────────

class TestPiiEmailDetection:
    """Email addresses in prompts should trigger a warning."""

    def test_single_email(self, runner):
        result = runner.run(make_prompt_input(
            "Send the report to admin@example.com please."
        ))
        assert result.has_warning
        assert "email" in result.additional_context.lower()

    def test_multiple_emails(self, runner):
        result = runner.run(make_prompt_input(
            "Contact user@test.com and support@company.org for help."
        ))
        assert result.has_warning
        assert "email" in result.additional_context.lower()


# ── SSN detection ───────────────────────────────────────────────────────────

class TestPiiSsnDetection:
    """Social Security Numbers should trigger a warning."""

    def test_ssn_dashed(self, runner):
        result = runner.run(make_prompt_input(
            "My SSN is 123-45-6789."
        ))
        assert result.has_warning
        assert "ssn" in result.additional_context.lower()


# ── AWS key detection ───────────────────────────────────────────────────────

class TestPiiAwsKeyDetection:
    """AWS access key IDs should trigger a warning."""

    def test_aws_key(self, runner):
        result = runner.run(make_prompt_input(
            "Here is my key: AKIA1234567890ABCDEF"
        ))
        assert result.has_warning
        assert "aws" in result.additional_context.lower()


# ── GitHub token detection ──────────────────────────────────────────────────

class TestPiiGithubTokenDetection:
    """GitHub personal access tokens should trigger a warning."""

    def test_github_pat(self, runner):
        result = runner.run(make_prompt_input(
            "Use token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl"
        ))
        assert result.has_warning
        assert "github" in result.additional_context.lower()

    def test_github_pat_new_format(self, runner):
        result = runner.run(make_prompt_input(
            "Token: github_pat_ABCDEFGHIJKLMNOPQRSTUV"
        ))
        assert result.has_warning
        assert "github" in result.additional_context.lower()


# ── Private key detection ──────────────────────────────────────────────────

class TestPiiPrivateKeyDetection:
    """Private key material should trigger a warning."""

    def test_rsa_private_key(self, runner):
        result = runner.run(make_prompt_input(
            "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA..."
        ))
        assert result.has_warning
        assert "private key" in result.additional_context.lower()

    def test_openssh_private_key(self, runner):
        result = runner.run(make_prompt_input(
            "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXk..."
        ))
        assert result.has_warning
        assert "private key" in result.additional_context.lower()


# ── Phone number detection ──────────────────────────────────────────────────

class TestPiiPhoneDetection:
    """Phone numbers should trigger a warning."""

    def test_us_phone_dashed(self, runner):
        result = runner.run(make_prompt_input(
            "Call me at 555-123-4567."
        ))
        assert result.has_warning
        assert "phone" in result.additional_context.lower()

    def test_us_phone_with_country_code(self, runner):
        result = runner.run(make_prompt_input(
            "Reach us at +1-555-123-4567."
        ))
        assert result.has_warning
        assert "phone" in result.additional_context.lower()


# ── Multiple PII types ─────────────────────────────────────────────────────

class TestPiiMultipleDetections:
    """Prompts with multiple PII types should report all of them."""

    def test_email_and_ssn(self, runner):
        result = runner.run(make_prompt_input(
            "My email is test@example.com and SSN is 123-45-6789."
        ))
        assert result.has_warning
        assert "email" in result.additional_context.lower()
        assert "ssn" in result.additional_context.lower()

    def test_email_and_aws_key(self, runner):
        result = runner.run(make_prompt_input(
            "Email: admin@example.com, AWS key: AKIA1234567890ABCDEF"
        ))
        assert result.has_warning
        assert "email" in result.additional_context.lower()
        assert "aws" in result.additional_context.lower()


# ── Exit code behavior ─────────────────────────────────────────────────────

class TestPiiExitCodes:
    """PII redactor always exits 0 — it never blocks."""

    def test_clean_prompt_exit_0(self, runner):
        result = runner.run(make_prompt_input("Normal question"))
        assert result.exit_code == 0

    def test_pii_prompt_exit_0(self, runner):
        result = runner.run(make_prompt_input("My SSN is 123-45-6789"))
        assert result.exit_code == 0

    def test_never_denies(self, runner):
        """Even with PII, the hook should never produce a deny decision."""
        result = runner.run(make_prompt_input(
            "AKIA1234567890ABCDEF password=secret123 admin@evil.com 123-45-6789"
        ))
        assert not result.is_deny
        assert result.has_warning


# ── Output format ──────────────────────────────────────────────────────────

class TestPiiOutputFormat:
    """Validate the structure of PII warning output."""

    def test_warning_has_additional_context(self, runner):
        result = runner.run(make_prompt_input("Email: user@test.com"))
        assert result.json_output is not None
        assert "additionalContext" in result.json_output

    def test_warning_mentions_pii_detection(self, runner):
        result = runner.run(make_prompt_input("SSN: 123-45-6789"))
        assert "PII Detection Warning" in result.additional_context

    def test_clean_prompt_no_json(self, runner):
        """Clean prompts should produce no JSON output (silent exit)."""
        result = runner.run(make_prompt_input("How do I write a for loop?"))
        assert result.json_output is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
