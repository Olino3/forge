# Package Manager Configuration

## Detected Manager

- **Manager**: poetry
- **Version**: 1.7.1
- **Detection Method**: Found poetry.lock in project root
- **Installation Path**: /usr/local/bin/poetry

## Configuration Files

- **Primary Config**: pyproject.toml
- **Lock File**: poetry.lock
- **Additional Files**: None

## Manager-Specific Notes

This project uses Poetry's recommended configuration:
- Dependencies in `[tool.poetry.dependencies]`
- Development dependencies in `[tool.poetry.group.dev.dependencies]`
- Virtual environment managed by Poetry (in cache directory)

Poetry is configured to use caret (^) version constraints by default for automatic semantic versioning compatibility.

## Detection History

- **First Detected**: 2025-11-14
- **Last Verified**: 2025-11-14
- **Changes**: None
