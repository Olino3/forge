# Developer Environment Engineer Agent Memory

This directory stores project-specific memory for the @developer-environment-engineer agent.

## Memory Structure

### projects/
Track development environment configurations per project:
- Services and their dependencies
- Container architecture
- Local infrastructure requirements
- Platform-specific configurations

### tooling/
Record development tools and utilities used:
- Build tools and versions
- Development dependencies
- Custom CLI tools and scripts
- IDE and editor configurations

### workflows/
Store developer workflow patterns and scripts:
- Common development tasks
- Build and test workflows
- Debugging configurations
- Deployment processes

### mock_services/
Maintain mock service configurations:
- Mock service endpoints
- Test data and fixtures
- API contract definitions
- Service virtualization strategies

## Usage

The agent will automatically create and update files in these subdirectories as it works on different projects. Each project gets its own subdirectory for isolated memory storage.
