#!/usr/bin/env python3
"""
Test Analyzer Helper Script

This script helps analyze existing Python test files to understand:
- Testing framework used (pytest, unittest, etc.)
- Test file naming conventions
- Fixture patterns
- Common test structures

Usage:
    python test_analyzer.py <test_directory>
    python test_analyzer.py <test_file.py>
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict


def analyze_test_file(file_path):
    """
    Analyze a single test file and extract patterns.

    Args:
        file_path: Path to the test file

    Returns:
        dict: Analysis results
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    analysis = {
        'file': str(file_path),
        'framework': detect_framework(content),
        'fixtures': find_fixtures(content),
        'test_count': count_tests(content),
        'uses_mocking': 'mock' in content.lower() or 'patch' in content,
        'uses_parametrize': '@pytest.mark.parametrize' in content,
        'test_classes': find_test_classes(content),
        'imports': extract_imports(content),
    }

    return analysis


def detect_framework(content):
    """Detect which testing framework is used."""
    if 'import pytest' in content or 'from pytest' in content:
        return 'pytest'
    elif 'import unittest' in content or 'from unittest' in content:
        return 'unittest'
    elif 'import nose' in content:
        return 'nose'
    else:
        return 'unknown'


def find_fixtures(content):
    """Find pytest fixtures in the file."""
    fixture_pattern = r'@pytest\.fixture(?:\([^)]*\))?\s+def\s+(\w+)'
    fixtures = re.findall(fixture_pattern, content)
    return fixtures


def count_tests(content):
    """Count the number of test functions/methods."""
    # Match both standalone functions and methods
    test_pattern = r'def\s+(test_\w+)'
    tests = re.findall(test_pattern, content)
    return len(tests)


def find_test_classes(content):
    """Find test classes."""
    class_pattern = r'class\s+(Test\w+)'
    classes = re.findall(class_pattern, content)
    return classes


def extract_imports(content):
    """Extract import statements."""
    import_lines = [
        line.strip()
        for line in content.split('\n')
        if line.strip().startswith(('import ', 'from '))
    ]
    return import_lines


def analyze_directory(directory):
    """
    Analyze all test files in a directory.

    Args:
        directory: Path to directory containing tests

    Returns:
        dict: Aggregate analysis results
    """
    test_files = find_test_files(directory)

    if not test_files:
        return {
            'error': f'No test files found in {directory}',
            'searched_patterns': ['test_*.py', '*_test.py']
        }

    analyses = [analyze_test_file(f) for f in test_files]

    # Aggregate results
    frameworks = defaultdict(int)
    all_fixtures = []
    total_tests = 0
    uses_mocking = 0
    uses_parametrize = 0

    for analysis in analyses:
        frameworks[analysis['framework']] += 1
        all_fixtures.extend(analysis['fixtures'])
        total_tests += analysis['test_count']
        if analysis['uses_mocking']:
            uses_mocking += 1
        if analysis['uses_parametrize']:
            uses_parametrize += 1

    return {
        'test_files_count': len(test_files),
        'total_tests': total_tests,
        'primary_framework': max(frameworks.items(), key=lambda x: x[1])[0] if frameworks else 'none',
        'frameworks': dict(frameworks),
        'common_fixtures': list(set(all_fixtures)),
        'mocking_usage': f'{uses_mocking}/{len(test_files)} files',
        'parametrize_usage': f'{uses_parametrize}/{len(test_files)} files',
        'test_files': [a['file'] for a in analyses],
        'naming_pattern': detect_naming_pattern(test_files),
    }


def find_test_files(directory):
    """Find all test files in directory."""
    test_files = []
    path = Path(directory)

    if path.is_file():
        return [path] if is_test_file(path) else []

    # Search for test files
    for pattern in ['test_*.py', '*_test.py']:
        test_files.extend(path.rglob(pattern))

    return sorted(test_files)


def is_test_file(file_path):
    """Check if a file is a test file."""
    name = file_path.name
    return (
        name.startswith('test_') or
        name.endswith('_test.py') or
        'test' in name.lower()
    ) and name.endswith('.py')


def detect_naming_pattern(test_files):
    """Detect the naming pattern used for test files."""
    if not test_files:
        return 'unknown'

    prefix_count = sum(1 for f in test_files if Path(f).name.startswith('test_'))
    suffix_count = sum(1 for f in test_files if Path(f).name.endswith('_test.py'))

    if prefix_count > suffix_count:
        return 'prefix (test_*.py)'
    elif suffix_count > prefix_count:
        return 'suffix (*_test.py)'
    else:
        return 'mixed'


def print_analysis(analysis):
    """Pretty print the analysis results."""
    if 'error' in analysis:
        print(f"Error: {analysis['error']}")
        print(f"Searched for: {', '.join(analysis['searched_patterns'])}")
        return

    print("=" * 60)
    print("PYTHON TEST ANALYSIS")
    print("=" * 60)
    print(f"\nTest Files Found: {analysis['test_files_count']}")
    print(f"Total Tests: {analysis['total_tests']}")
    print(f"Primary Framework: {analysis['primary_framework']}")
    print(f"Naming Pattern: {analysis['naming_pattern']}")
    print(f"\nMocking Usage: {analysis['mocking_usage']}")
    print(f"Parametrize Usage: {analysis['parametrize_usage']}")

    if analysis['common_fixtures']:
        print(f"\nCommon Fixtures ({len(analysis['common_fixtures'])}):")
        for fixture in sorted(analysis['common_fixtures'])[:10]:
            print(f"  - {fixture}")
        if len(analysis['common_fixtures']) > 10:
            print(f"  ... and {len(analysis['common_fixtures']) - 10} more")

    print(f"\nTest Files:")
    for file_path in analysis['test_files'][:5]:
        print(f"  - {file_path}")
    if len(analysis['test_files']) > 5:
        print(f"  ... and {len(analysis['test_files']) - 5} more")

    print("=" * 60)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python test_analyzer.py <test_directory_or_file>")
        print("\nExample:")
        print("  python test_analyzer.py tests/")
        print("  python test_analyzer.py tests/test_user_service.py")
        sys.exit(1)

    target = sys.argv[1]

    if not os.path.exists(target):
        print(f"Error: Path '{target}' does not exist")
        sys.exit(1)

    if os.path.isfile(target):
        # Analyze single file
        analysis = analyze_test_file(target)
        print("=" * 60)
        print(f"ANALYSIS: {analysis['file']}")
        print("=" * 60)
        print(f"Framework: {analysis['framework']}")
        print(f"Test Count: {analysis['test_count']}")
        print(f"Test Classes: {', '.join(analysis['test_classes']) or 'None'}")
        print(f"Fixtures: {', '.join(analysis['fixtures']) or 'None'}")
        print(f"Uses Mocking: {analysis['uses_mocking']}")
        print(f"Uses Parametrize: {analysis['uses_parametrize']}")
    else:
        # Analyze directory
        analysis = analyze_directory(target)
        print_analysis(analysis)


if __name__ == '__main__':
    main()
