#!/usr/bin/env python3
"""
Results Parser and Aggregator

Parses and aggregates results from various code analysis tools
into a unified, human-readable format.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


class ResultsParser:
    """Parse and aggregate code review results."""

    def __init__(self, results_dir: str = "review_results"):
        self.results_dir = Path(results_dir)
        self.aggregated = {
            "critical": [],
            "important": [],
            "minor": [],
            "info": []
        }

    def load_results(self) -> Dict:
        """Load all results from JSON file."""
        results_file = self.results_dir / "all_results.json"

        if not results_file.exists():
            print(f"Error: Results file not found: {results_file}")
            return {}

        with open(results_file) as f:
            return json.load(f)

    def parse_bandit(self, results: Dict) -> List[Dict]:
        """Parse bandit security scan results."""
        issues = []

        if "error" in results:
            return issues

        for issue in results.get("issues", []):
            severity = issue.get("issue_severity", "MEDIUM")
            confidence = issue.get("issue_confidence", "MEDIUM")

            # Map to our severity levels
            if severity == "HIGH":
                level = "critical"
            elif severity == "MEDIUM" and confidence == "HIGH":
                level = "important"
            else:
                level = "minor"

            issues.append({
                "level": level,
                "tool": "bandit",
                "category": "Security",
                "title": issue.get("issue_text", "Security issue"),
                "file": issue.get("filename", "unknown"),
                "line": issue.get("line_number", 0),
                "description": issue.get("issue_text", ""),
                "severity": severity,
                "confidence": confidence,
                "cwe": issue.get("issue_cwe", {}).get("id", "N/A")
            })

        return issues

    def parse_mypy(self, results: Dict) -> List[Dict]:
        """Parse mypy type checking results."""
        issues = []

        if "error" in results:
            return issues

        for error in results.get("errors", []):
            # Parse mypy error format: "file.py:line: error: message [error-code]"
            parts = error.split(":")
            if len(parts) >= 4:
                file = parts[0].strip()
                line = parts[1].strip()
                message = ":".join(parts[3:]).strip()

                issues.append({
                    "level": "important",
                    "tool": "mypy",
                    "category": "Type Safety",
                    "title": "Type error",
                    "file": file,
                    "line": line,
                    "description": message
                })

        return issues

    def parse_radon(self, results: Dict) -> List[Dict]:
        """Parse radon complexity analysis results."""
        issues = []

        if "error" in results:
            return issues

        for func in results.get("complex_functions", []):
            complexity = func.get("complexity", 0)

            # Map complexity to severity
            if complexity > 20:
                level = "important"
            elif complexity > 10:
                level = "minor"
            else:
                level = "info"

            issues.append({
                "level": level,
                "tool": "radon",
                "category": "Complexity",
                "title": f"High complexity in {func.get('function', 'unknown')}",
                "file": func.get("file", "unknown"),
                "line": 0,
                "description": f"Cyclomatic complexity: {complexity} (Rank: {func.get('rank', 'N/A')})",
                "complexity": complexity
            })

        return issues

    def parse_vulture(self, results: Dict) -> List[Dict]:
        """Parse vulture dead code detection results."""
        issues = []

        if "error" in results:
            return issues

        for dead_code in results.get("dead_code", []):
            # Parse vulture format: "file.py:line: unused variable 'name' (80% confidence)"
            if ":" in dead_code:
                parts = dead_code.split(":")
                if len(parts) >= 3:
                    file = parts[0].strip()
                    line = parts[1].strip()
                    message = ":".join(parts[2:]).strip()

                    issues.append({
                        "level": "minor",
                        "tool": "vulture",
                        "category": "Dead Code",
                        "title": "Unused code detected",
                        "file": file,
                        "line": line,
                        "description": message
                    })

        return issues

    def parse_safety(self, results: Dict) -> List[Dict]:
        """Parse safety dependency vulnerability results."""
        issues = []

        if "error" in results:
            return issues

        for vuln in results.get("vulnerabilities", []):
            issues.append({
                "level": "critical",
                "tool": "safety",
                "category": "Dependency",
                "title": f"Vulnerable dependency: {vuln.get('package', 'unknown')}",
                "file": "requirements.txt",
                "line": 0,
                "description": vuln.get("advisory", "Security vulnerability in dependency"),
                "package": vuln.get("package", "unknown"),
                "installed_version": vuln.get("installed_version", "unknown"),
                "affected_versions": vuln.get("affected_versions", "unknown"),
                "fix": f"Upgrade to {vuln.get('safe_version', 'latest version')}" if vuln.get("safe_version") else "Check for updates"
            })

        return issues

    def aggregate_results(self, results: Dict):
        """Aggregate all results by severity."""
        if "bandit" in results:
            issues = self.parse_bandit(results["bandit"])
            for issue in issues:
                self.aggregated[issue["level"]].append(issue)

        if "mypy" in results:
            issues = self.parse_mypy(results["mypy"])
            for issue in issues:
                self.aggregated[issue["level"]].append(issue)

        if "radon" in results:
            issues = self.parse_radon(results["radon"])
            for issue in issues:
                self.aggregated[issue["level"]].append(issue)

        if "vulture" in results:
            issues = self.parse_vulture(results["vulture"])
            for issue in issues:
                self.aggregated[issue["level"]].append(issue)

        if "safety" in results:
            issues = self.parse_safety(results["safety"])
            for issue in issues:
                self.aggregated[issue["level"]].append(issue)

    def generate_markdown_report(self, output_file: str = "code_review_report.md"):
        """Generate a markdown report from aggregated results."""
        output_path = self.results_dir / output_file

        with open(output_path, 'w') as f:
            f.write("# Code Review Report\n\n")
            f.write("## Summary\n\n")

            total_issues = sum(len(issues) for issues in self.aggregated.values())
            f.write(f"- **Total Issues**: {total_issues}\n")
            f.write(f"- **Critical**: {len(self.aggregated['critical'])}\n")
            f.write(f"- **Important**: {len(self.aggregated['important'])}\n")
            f.write(f"- **Minor**: {len(self.aggregated['minor'])}\n")
            f.write(f"- **Info**: {len(self.aggregated['info'])}\n\n")

            # Critical issues
            if self.aggregated['critical']:
                f.write("## Critical Issues\n\n")
                for issue in self.aggregated['critical']:
                    f.write(f"### {issue['title']}\n\n")
                    f.write(f"- **Category**: {issue['category']}\n")
                    f.write(f"- **File**: `{issue['file']}:{issue['line']}`\n")
                    f.write(f"- **Tool**: {issue['tool']}\n")
                    f.write(f"- **Description**: {issue['description']}\n")
                    if 'fix' in issue:
                        f.write(f"- **Fix**: {issue['fix']}\n")
                    f.write("\n")

            # Important issues
            if self.aggregated['important']:
                f.write("## Important Issues\n\n")
                for issue in self.aggregated['important']:
                    f.write(f"### {issue['title']}\n\n")
                    f.write(f"- **Category**: {issue['category']}\n")
                    f.write(f"- **File**: `{issue['file']}:{issue['line']}`\n")
                    f.write(f"- **Tool**: {issue['tool']}\n")
                    f.write(f"- **Description**: {issue['description']}\n\n")

            # Minor issues (summarized)
            if self.aggregated['minor']:
                f.write("## Minor Issues\n\n")
                f.write(f"Found {len(self.aggregated['minor'])} minor issues. ")
                f.write("Run detailed analysis for full list.\n\n")

                # Group by category
                by_category = defaultdict(list)
                for issue in self.aggregated['minor']:
                    by_category[issue['category']].append(issue)

                for category, issues in by_category.items():
                    f.write(f"- **{category}**: {len(issues)} issues\n")

        print(f"\nMarkdown report generated: {output_path}")
        return output_path

    def print_summary(self):
        """Print summary to console."""
        print("\n" + "="*60)
        print("CODE REVIEW SUMMARY")
        print("="*60 + "\n")

        total = sum(len(issues) for issues in self.aggregated.values())
        print(f"Total Issues: {total}\n")

        if self.aggregated['critical']:
            print(f"[!] CRITICAL ({len(self.aggregated['critical'])})")
            for issue in self.aggregated['critical']:
                print(f"  - {issue['file']}:{issue['line']} - {issue['title']}")
            print()

        if self.aggregated['important']:
            print(f"[!] IMPORTANT ({len(self.aggregated['important'])})")
            for issue in self.aggregated['important'][:5]:  # Show top 5
                print(f"  - {issue['file']}:{issue['line']} - {issue['title']}")
            if len(self.aggregated['important']) > 5:
                print(f"  ... and {len(self.aggregated['important']) - 5} more")
            print()

        print(f"[i] Minor: {len(self.aggregated['minor'])}")
        print(f"[i] Info: {len(self.aggregated['info'])}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Parse and aggregate code review results"
    )
    parser.add_argument(
        "-d", "--dir",
        default="review_results",
        help="Results directory (default: review_results)"
    )
    parser.add_argument(
        "-o", "--output",
        default="code_review_report.md",
        help="Output markdown file (default: code_review_report.md)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Also output JSON format"
    )

    args = parser.parse_args()

    parser_tool = ResultsParser(args.dir)

    # Load and aggregate results
    results = parser_tool.load_results()
    if not results:
        return

    parser_tool.aggregate_results(results)

    # Print summary
    parser_tool.print_summary()

    # Generate markdown report
    parser_tool.generate_markdown_report(args.output)

    # Optionally save JSON
    if args.json:
        json_file = Path(args.dir) / "aggregated_results.json"
        with open(json_file, 'w') as f:
            json.dump(parser_tool.aggregated, f, indent=2)
        print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()
