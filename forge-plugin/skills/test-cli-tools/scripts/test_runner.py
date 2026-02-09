#!/usr/bin/env python3
"""
CLI Test Runner Helper

This script provides utilities for running and validating CLI commands
during the test-cli-tools skill execution.

Usage:
    python test_runner.py run <command>
    python test_runner.py validate <command> --expected-exit-code 0
"""

import subprocess
import sys
import time
import json
from typing import Tuple, Dict, Any


def run_command(command: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Run a CLI command and capture all output.

    Args:
        command: Command string to execute
        timeout: Maximum execution time in seconds

    Returns:
        Dictionary containing:
        - command: Original command
        - exit_code: Process exit code
        - stdout: Standard output
        - stderr: Standard error
        - duration: Execution time in seconds
        - success: Boolean indicating if exit code was 0
    """
    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        duration = time.time() - start_time

        return {
            "command": command,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration,
            "success": result.returncode == 0,
            "timed_out": False
        }

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time

        return {
            "command": command,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "duration": duration,
            "success": False,
            "timed_out": True
        }

    except Exception as e:
        duration = time.time() - start_time

        return {
            "command": command,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": duration,
            "success": False,
            "timed_out": False
        }


def validate_command(
    command: str,
    expected_exit_code: int = 0,
    expected_output_contains: str = None,
    should_error: bool = False
) -> Tuple[bool, str]:
    """
    Run a command and validate its behavior.

    Args:
        command: Command to test
        expected_exit_code: Expected exit code
        expected_output_contains: String that should be in output
        should_error: Whether command should produce stderr

    Returns:
        Tuple of (passed: bool, message: str)
    """
    result = run_command(command)

    # Check exit code
    if result["exit_code"] != expected_exit_code:
        return False, f"Expected exit code {expected_exit_code}, got {result['exit_code']}"

    # Check for expected output
    if expected_output_contains:
        combined_output = result["stdout"] + result["stderr"]
        if expected_output_contains not in combined_output:
            return False, f"Expected output to contain '{expected_output_contains}'"

    # Check error expectation
    if should_error and not result["stderr"]:
        return False, "Expected stderr output, but got none"

    if not should_error and result["stderr"] and result["success"]:
        # Having stderr on success might be a warning, which is acceptable
        pass

    return True, "Command passed validation"


def format_test_result(result: Dict[str, Any], passed: bool = None) -> str:
    """
    Format test result for display.

    Args:
        result: Result dictionary from run_command
        passed: Optional override for pass/fail status

    Returns:
        Formatted string for display
    """
    if passed is None:
        passed = result["success"]

    status = "✓ PASS" if passed else "✗ FAIL"
    duration_str = f"{result['duration']:.2f}s"

    output = [
        f"{status} - {result['command']}",
        f"Exit Code: {result['exit_code']}",
        f"Duration: {duration_str}"
    ]

    if result["stdout"]:
        output.append(f"stdout: {result['stdout'][:200]}")

    if result["stderr"]:
        output.append(f"stderr: {result['stderr'][:200]}")

    return "\n".join(output)


def extract_commands_from_help(help_output: str) -> list:
    """
    Parse --help output to extract available commands.

    Args:
        help_output: Output from running `tool --help`

    Returns:
        List of command names
    """
    commands = []
    in_commands_section = False

    for line in help_output.split('\n'):
        line = line.strip()

        # Detect commands section
        if 'command' in line.lower() and ':' in line:
            in_commands_section = True
            continue

        # Exit commands section on empty line or new section
        if in_commands_section:
            if not line or (':' in line and not line.startswith(' ')):
                in_commands_section = False
                continue

            # Extract command name (first word)
            if line and not line.startswith('-'):
                parts = line.split()
                if parts:
                    commands.append(parts[0])

    return commands


def categorize_command_risk(command: str) -> str:
    """
    Categorize command by risk level.

    Args:
        command: Command name

    Returns:
        Risk level: 'safe', 'moderate', or 'destructive'
    """
    destructive_keywords = [
        'delete', 'remove', 'rm', 'destroy', 'drop', 'purge',
        'erase', 'wipe', 'clear', 'reset', 'format'
    ]

    moderate_keywords = [
        'create', 'add', 'update', 'modify', 'set', 'configure',
        'install', 'deploy', 'apply', 'push', 'publish'
    ]

    safe_keywords = [
        'list', 'get', 'show', 'describe', 'info', 'status',
        'version', 'help', 'search', 'find', 'view', 'read'
    ]

    command_lower = command.lower()

    # Check destructive first (highest risk)
    if any(keyword in command_lower for keyword in destructive_keywords):
        return 'destructive'

    # Check safe next
    if any(keyword in command_lower for keyword in safe_keywords):
        return 'safe'

    # Check moderate
    if any(keyword in command_lower for keyword in moderate_keywords):
        return 'moderate'

    # Default to moderate if unclear
    return 'moderate'


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  test_runner.py run <command>")
        print("  test_runner.py validate <command> [--expected-exit-code CODE]")
        print("  test_runner.py categorize <command>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "run":
        if len(sys.argv) < 3:
            print("Error: No command specified")
            sys.exit(1)

        command = " ".join(sys.argv[2:])
        result = run_command(command)
        print(json.dumps(result, indent=2))

    elif action == "validate":
        if len(sys.argv) < 3:
            print("Error: No command specified")
            sys.exit(1)

        # Extract command (everything before --expected-exit-code if present)
        if "--expected-exit-code" in sys.argv:
            idx = sys.argv.index("--expected-exit-code")
            command = " ".join(sys.argv[2:idx])
        else:
            command = " ".join(sys.argv[2:])
        expected_code = 0

        if "--expected-exit-code" in sys.argv:
            idx = sys.argv.index("--expected-exit-code")
            if idx + 1 >= len(sys.argv):
                print("Error: --expected-exit-code requires a value")
                sys.exit(1)
            expected_code = int(sys.argv[idx + 1])

        passed, message = validate_command(command, expected_exit_code=expected_code)
        print(f"Result: {'PASS' if passed else 'FAIL'}")
        print(f"Message: {message}")
        sys.exit(0 if passed else 1)

    elif action == "categorize":
        if len(sys.argv) < 3:
            print("Error: No command specified")
            sys.exit(1)

        command = sys.argv[2]
        risk = categorize_command_risk(command)
        print(f"Risk Level: {risk}")

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
