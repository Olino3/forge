#!/usr/bin/env python3
"""
Azure Functions Project Generator Helper

This script provides utilities for generating Azure Functions projects
during the generate-azure-functions skill execution.

Usage:
    python project_generator.py generate-key
    python project_generator.py validate-config <config-file>
    python project_generator.py list-base-images <runtime>
"""

import sys
import secrets
import base64
import json
import os
from typing import Dict, List, Any


def generate_azurite_key() -> str:
    """
    Generate a random Azurite account key.

    Returns:
        Base64-encoded random key (64 bytes)
    """
    # Generate 64 random bytes
    random_bytes = secrets.token_bytes(64)
    # Encode as base64
    key = base64.b64encode(random_bytes).decode('utf-8')
    return key


def get_base_image(runtime: str, version: str) -> str:
    """
    Get the appropriate Azure Functions base Docker image.

    Args:
        runtime: Runtime name (python, node, dotnet)
        version: Version string (e.g., "3.11", "18", "8")

    Returns:
        Docker image reference
    """
    base_images = {
        "python": {
            "3.9": "mcr.microsoft.com/azure-functions/python:4-python3.9",
            "3.10": "mcr.microsoft.com/azure-functions/python:4-python3.10",
            "3.11": "mcr.microsoft.com/azure-functions/python:4-python3.11",
        },
        "node": {
            "16": "mcr.microsoft.com/azure-functions/node:4-node16",
            "18": "mcr.microsoft.com/azure-functions/node:4-node18",
            "20": "mcr.microsoft.com/azure-functions/node:4-node20",
        },
        "dotnet": {
            "6": "mcr.microsoft.com/azure-functions/dotnet-isolated:4-dotnet-isolated6.0",
            "7": "mcr.microsoft.com/azure-functions/dotnet-isolated:4-dotnet-isolated7.0",
            "8": "mcr.microsoft.com/azure-functions/dotnet-isolated:4-dotnet-isolated8.0",
        }
    }

    runtime_lower = runtime.lower()
    if runtime_lower not in base_images:
        raise ValueError(f"Unknown runtime: {runtime}. Supported: {list(base_images.keys())}")

    if version not in base_images[runtime_lower]:
        available = list(base_images[runtime_lower].keys())
        raise ValueError(f"Unknown version '{version}' for runtime '{runtime}'. Supported: {available}")

    return base_images[runtime_lower][version]


def list_base_images(runtime: str = None) -> Dict[str, Dict[str, str]]:
    """
    List all available base images.

    Args:
        runtime: Optional runtime filter (python, node, dotnet)

    Returns:
        Dictionary of runtime -> version -> image
    """
    base_images = {
        "python": {
            "3.9": "mcr.microsoft.com/azure-functions/python:4-python3.9",
            "3.10": "mcr.microsoft.com/azure-functions/python:4-python3.10",
            "3.11": "mcr.microsoft.com/azure-functions/python:4-python3.11",
        },
        "node": {
            "16": "mcr.microsoft.com/azure-functions/node:4-node16",
            "18": "mcr.microsoft.com/azure-functions/node:4-node18",
            "20": "mcr.microsoft.com/azure-functions/node:4-node20",
        },
        "dotnet": {
            "6": "mcr.microsoft.com/azure-functions/dotnet-isolated:4-dotnet-isolated6.0",
            "7": "mcr.microsoft.com/azure-functions/dotnet-isolated:4-dotnet-isolated7.0",
            "8": "mcr.microsoft.com/azure-functions/dotnet-isolated:4-dotnet-isolated8.0",
        }
    }

    if runtime:
        runtime_lower = runtime.lower()
        if runtime_lower not in base_images:
            raise ValueError(f"Unknown runtime: {runtime}")
        return {runtime_lower: base_images[runtime_lower]}

    return base_images


def validate_project_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate project configuration.

    Args:
        config: Project configuration dictionary

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Required fields
    required_fields = ['project_name', 'runtime', 'programming_model', 'function_apps']
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")

    # Validate runtime
    if 'runtime' in config:
        runtime = config['runtime']
        if 'name' not in runtime:
            errors.append("Runtime must have 'name' field")
        if 'version' not in runtime:
            errors.append("Runtime must have 'version' field")
        else:
            # Validate runtime/version combination
            try:
                get_base_image(runtime.get('name', ''), runtime.get('version', ''))
            except ValueError as e:
                errors.append(str(e))

    # Validate function apps
    if 'function_apps' in config:
        function_apps = config['function_apps']
        if not isinstance(function_apps, list):
            errors.append("function_apps must be a list")
        elif len(function_apps) == 0:
            errors.append("Must have at least one function app")
        else:
            # Check for duplicate names
            names = [app.get('name') for app in function_apps]
            if len(names) != len(set(names)):
                errors.append("Function app names must be unique")

            # Validate each function app
            for i, app in enumerate(function_apps):
                if 'name' not in app:
                    errors.append(f"Function app {i} missing 'name' field")
                if 'port' not in app:
                    errors.append(f"Function app {i} missing 'port' field")
                elif not isinstance(app['port'], int) or app['port'] < 1024 or app['port'] > 65535:
                    errors.append(f"Function app {i} port must be between 1024 and 65535")

    # Validate programming model
    if 'programming_model' in config:
        model = config['programming_model']
        valid_models = ['v1', 'v2', 'v4']  # v4 for Node.js
        if model not in valid_models:
            errors.append(f"Invalid programming model: {model}. Must be one of {valid_models}")

    # Validate storage resources
    if 'storage' in config:
        storage = config['storage']
        for resource_type in ['blob_containers', 'queues', 'tables']:
            if resource_type in storage:
                resources = storage[resource_type]
                if not isinstance(resources, list):
                    errors.append(f"storage.{resource_type} must be a list")
                else:
                    for resource in resources:
                        if 'name' not in resource:
                            errors.append(f"storage.{resource_type} item missing 'name' field")

    return errors


def generate_port_assignments(num_function_apps: int, start_port: int = 7071) -> List[int]:
    """
    Generate sequential port assignments for function apps.

    Args:
        num_function_apps: Number of function apps
        start_port: Starting port number (default: 7071)

    Returns:
        List of port numbers
    """
    return list(range(start_port, start_port + num_function_apps))


def detect_programming_model(function_path: str) -> str:
    """
    Detect programming model from existing function code.

    Args:
        function_path: Path to function directory

    Returns:
        Programming model ('v1' or 'v2' for Python, 'v4' for Node.js)
    """
    # Check for function_app.py (v2 Python)
    if os.path.exists(os.path.join(function_path, 'function_app.py')):
        return 'v2'

    # Check for function.json files (v1 Python or Node.js)
    for item in os.listdir(function_path):
        item_path = os.path.join(function_path, item)
        if os.path.isdir(item_path):
            if os.path.exists(os.path.join(item_path, 'function.json')):
                # Check if it's Node.js or Python
                if os.path.exists(os.path.join(item_path, 'index.js')) or \
                   os.path.exists(os.path.join(item_path, 'index.ts')):
                    return 'v4'  # Node.js
                else:
                    return 'v1'  # Python v1

    # Default to v2
    return 'v2'


def get_default_storage_resources(function_types: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """
    Get default storage resources based on function types.

    Args:
        function_types: List of function types (http, blob, queue, timer, etc.)

    Returns:
        Dictionary with blob_containers, queues, and tables
    """
    resources = {
        'blob_containers': [],
        'queues': [],
        'tables': []
    }

    # Add default resources based on function types
    if 'blob' in function_types:
        resources['blob_containers'].extend([
            {'name': 'uploads', 'description': 'Uploaded files'},
            {'name': 'processed', 'description': 'Processed files'}
        ])

    if 'queue' in function_types:
        resources['queues'].append({
            'name': 'tasks',
            'description': 'Task processing queue'
        })

    if 'http' in function_types or 'timer' in function_types:
        # Always add a basic blob container for general use
        if not any(c['name'] == 'data' for c in resources['blob_containers']):
            resources['blob_containers'].append({
                'name': 'data',
                'description': 'General data storage'
            })

    # Always add an audit log table
    resources['tables'].append({
        'name': 'AuditLog',
        'description': 'Application audit log'
    })

    return resources


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  project_generator.py generate-key")
        print("  project_generator.py get-base-image <runtime> <version>")
        print("  project_generator.py list-base-images [runtime]")
        print("  project_generator.py validate-config <config-file>")
        print("  project_generator.py generate-ports <count> [start-port]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "generate-key":
        key = generate_azurite_key()
        print(key)

    elif action == "get-base-image":
        if len(sys.argv) < 4:
            print("Error: Missing runtime or version")
            print("Usage: project_generator.py get-base-image <runtime> <version>")
            sys.exit(1)

        runtime = sys.argv[2]
        version = sys.argv[3]

        try:
            image = get_base_image(runtime, version)
            print(image)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif action == "list-base-images":
        runtime = sys.argv[2] if len(sys.argv) > 2 else None

        try:
            images = list_base_images(runtime)
            print(json.dumps(images, indent=2))
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif action == "validate-config":
        if len(sys.argv) < 3:
            print("Error: Missing config file")
            print("Usage: project_generator.py validate-config <config-file>")
            sys.exit(1)

        config_file = sys.argv[2]

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)

            errors = validate_project_config(config)

            if errors:
                print("Configuration validation failed:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            else:
                print("Configuration is valid")
        except FileNotFoundError:
            print(f"Error: Config file not found: {config_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config file: {e}")
            sys.exit(1)

    elif action == "generate-ports":
        if len(sys.argv) < 3:
            print("Error: Missing count")
            print("Usage: project_generator.py generate-ports <count> [start-port]")
            sys.exit(1)

        count = int(sys.argv[2])
        start_port = int(sys.argv[3]) if len(sys.argv) > 3 else 7071

        ports = generate_port_assignments(count, start_port)
        print(json.dumps(ports))

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
