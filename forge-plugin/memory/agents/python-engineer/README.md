# Python Engineer Agent Memory

This directory stores project-specific memory for the @python-engineer agent.

## Memory Structure

### projects/
Track Python projects, frameworks, and configurations:
- Python version used
- Framework choice (Django, Flask, FastAPI, etc.)
- Project architecture and structure
- Key dependencies and their purpose

### patterns/
Store project-specific coding patterns and conventions:
- Code organization patterns
- Naming conventions
- Design patterns used
- Team-specific preferences

### dependencies/
Maintain dependency management strategies:
- Package management tool (pip, poetry, pipenv)
- Virtual environment setup
- Dependency pinning strategy
- Update and maintenance approaches

### testing/
Record testing approaches and configurations:
- Testing framework (pytest, unittest)
- Coverage targets
- Test organization patterns
- Mock and fixture strategies

## Usage

The agent will automatically create and update files in these subdirectories as it works on different projects. Each project gets its own subdirectory for isolated memory storage.
