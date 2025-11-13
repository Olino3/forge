#!/usr/bin/env python3
"""
Automated Code Review Runner

Orchestrates multiple code analysis tools for security, complexity, and quality checks.
Uses modern Python toolchain: ruff, basedpyright, isort, bandit, safety.
Focuses on substantive issues that require manual review, not style/formatting.
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import shutil


class ReviewRunner:
    """Runs automated code review tools and collects results."""

    def __init__(self, target_path: str, output_dir: str = "review_results"):
        self.target_path = Path(target_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}

    def check_tool_installed(self, tool: str) -> bool:
        """Check if a tool is installed and available."""
        return shutil.which(tool) is not None

    def run_ruff(self) -> Dict:
        """Run ruff for linting and code quality checks."""
        print("[+] Running ruff (linter and formatter)...")

        if not self.check_tool_installed("ruff"):
            return {"error": "ruff not installed. Install with: pip install ruff"}

        output_file = self.output_dir / "ruff_results.json"

        cmd = [
            "ruff",
            "check",
            str(self.target_path),
            "--output-format=json",
            "--select", "E,F,W,C,N,UP,B,A,COM,S,T20,SIM,TCH,ARG,PTH,PL,RUF",
            "--ignore", "E501"  # Line length handled by formatter
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.stdout.strip():
                issues = json.loads(result.stdout)
            else:
                issues = []

            with open(output_file, "w") as f:
                json.dump(issues, f, indent=2)

            print(f"  Found {len(issues)} linting issues")

            return {
                "tool": "ruff",
                "issues": issues,
                "summary": {"total": len(issues)}
            }

        except subprocess.TimeoutExpired:
            return {"error": "ruff timed out"}
        except Exception as e:
            return {"error": f"ruff failed: {str(e)}"}

    def run_basedpyright(self) -> Dict:
        """Run basedpyright for type checking."""
        print("[+] Running basedpyright (type checker)...")

        if not self.check_tool_installed("basedpyright"):
            return {"error": "basedpyright not installed. Install with: pip install basedpyright"}

        output_file = self.output_dir / "basedpyright_results.json"

        cmd = [
            "basedpyright",
            str(self.target_path),
            "--outputjson"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.stdout.strip():
                data = json.loads(result.stdout)
                diagnostics = data.get("generalDiagnostics", [])
            else:
                diagnostics = []

            with open(output_file, "w") as f:
                json.dump(diagnostics, f, indent=2)

            print(f"  Found {len(diagnostics)} type errors")

            return {
                "tool": "basedpyright",
                "diagnostics": diagnostics,
                "summary": {"total": len(diagnostics)}
            }

        except subprocess.TimeoutExpired:
            return {"error": "basedpyright timed out"}
        except Exception as e:
            return {"error": f"basedpyright failed: {str(e)}"}

    def run_isort_check(self) -> Dict:
        """Check import sorting with isort."""
        print("[+] Running isort (import sorter check)...")

        if not self.check_tool_installed("isort"):
            return {"error": "isort not installed. Install with: pip install isort"}

        cmd = [
            "isort",
            str(self.target_path),
            "--check-only",
            "--diff"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # isort returns non-zero if changes would be made
            issues = []
            if result.returncode != 0 and result.stdout:
                issues = result.stdout.split("\n")

            print(f"  Found {len(issues)} import sorting issues")

            return {
                "tool": "isort",
                "issues": issues,
                "summary": {"total": len([i for i in issues if i.strip()])}
            }

        except subprocess.TimeoutExpired:
            return {"error": "isort timed out"}
        except Exception as e:
            return {"error": f"isort failed: {str(e)}"}


    def run_bandit(self) -> Dict:
        """Run bandit for security vulnerability scanning."""
        print("[+] Running bandit (security scanner)...")

        if not self.check_tool_installed("bandit"):
            return {"error": "bandit not installed. Install with: pip install bandit"}

        output_file = self.output_dir / "bandit_results.json"

        cmd = [
            "bandit",
            "-r", str(self.target_path),
            "-f", "json",
            "-o", str(output_file),
            "-ll"  # Only report medium and high severity
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            with open(output_file) as f:
                data = json.load(f)

            issues = data.get("results", [])
            print(f"  Found {len(issues)} security issues")

            return {
                "tool": "bandit",
                "issues": issues,
                "summary": {
                    "total": len(issues),
                    "high": sum(1 for i in issues if i.get("issue_severity") == "HIGH"),
                    "medium": sum(1 for i in issues if i.get("issue_severity") == "MEDIUM")
                }
            }

        except subprocess.TimeoutExpired:
            return {"error": "bandit timed out"}
        except Exception as e:
            return {"error": f"bandit failed: {str(e)}"}

    def run_safety(self) -> Dict:
        """Run safety for dependency vulnerability check."""
        print("[+] Running safety (dependency scanner)...")

        if not self.check_tool_installed("safety"):
            return {"error": "safety not installed. Install with: pip install safety"}

        output_file = self.output_dir / "safety_results.json"

        cmd = [
            "safety",
            "check",
            "--json",
            "--output", str(output_file)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # Safety exits with 64 if vulnerabilities found
            if output_file.exists():
                with open(output_file) as f:
                    data = json.load(f)

                vulnerabilities = data if isinstance(data, list) else []
                print(f"  Found {len(vulnerabilities)} vulnerable dependencies")

                return {
                    "tool": "safety",
                    "vulnerabilities": vulnerabilities,
                    "summary": {"total": len(vulnerabilities)}
                }
            else:
                print("  No vulnerabilities found")
                return {
                    "tool": "safety",
                    "vulnerabilities": [],
                    "summary": {"total": 0}
                }

        except subprocess.TimeoutExpired:
            return {"error": "safety timed out"}
        except Exception as e:
            return {"error": f"safety failed: {str(e)}"}

    def run_all(self) -> Dict:
        """Run all analysis tools."""
        print(f"\n{'='*60}")
        print(f"Running automated code review on: {self.target_path}")
        print(f"{'='*60}\n")

        self.results = {
            "ruff": self.run_ruff(),
            "basedpyright": self.run_basedpyright(),
            "isort": self.run_isort_check(),
            "bandit": self.run_bandit(),
            "safety": self.run_safety()
        }

        # Save aggregated results
        results_file = self.output_dir / "all_results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n{'='*60}")
        print(f"Results saved to: {self.output_dir}")
        print(f"{'='*60}\n")

        return self.results

    def print_summary(self):
        """Print summary of all results."""
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60 + "\n")

        for tool, result in self.results.items():
            if "error" in result:
                print(f"[!] {tool.upper()}: {result['error']}")
            elif "summary" in result:
                summary = result["summary"]
                total = summary.get("total", 0)

                if total > 0:
                    print(f"[!] {tool.upper()}: {total} issues found")
                    if "high" in summary:
                        print(f"    - High severity: {summary['high']}")
                    if "medium" in summary:
                        print(f"    - Medium severity: {summary['medium']}")
                else:
                    print(f"[✓] {tool.upper()}: No issues found")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="Run automated code review tools"
    )
    parser.add_argument(
        "path",
        help="Path to Python file or directory to analyze"
    )
    parser.add_argument(
        "-o", "--output",
        default="review_results",
        help="Output directory for results (default: review_results)"
    )
    parser.add_argument(
        "--tools",
        nargs="+",
        choices=["ruff", "basedpyright", "isort", "bandit", "safety", "all"],
        default=["all"],
        help="Tools to run (default: all)"
    )

    args = parser.parse_args()

    runner = ReviewRunner(args.path, args.output)

    if "all" in args.tools:
        runner.run_all()
    else:
        # Run selected tools
        if "ruff" in args.tools:
            runner.results["ruff"] = runner.run_ruff()
        if "basedpyright" in args.tools:
            runner.results["basedpyright"] = runner.run_basedpyright()
        if "isort" in args.tools:
            runner.results["isort"] = runner.run_isort_check()
        if "bandit" in args.tools:
            runner.results["bandit"] = runner.run_bandit()
        if "safety" in args.tools:
            runner.results["safety"] = runner.run_safety()

    runner.print_summary()


if __name__ == "__main__":
    main()
