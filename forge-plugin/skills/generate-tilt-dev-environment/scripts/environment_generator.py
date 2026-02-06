#!/usr/bin/env python3
"""
Environment Generator Helper Script
Assists with generating Tilt development environment configurations
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

def detect_project_type(project_path: str) -> Dict[str, any]:
    """
    Detect project type based on files in directory
    
    Returns:
        dict: Project information including type, languages, frameworks
    """
    path = Path(project_path)
    info = {
        'languages': [],
        'frameworks': [],
        'databases': [],
        'config_files': []
    }
    
    # Check for language-specific files
    if (path / 'package.json').exists():
        info['languages'].append('Node.js')
        info['config_files'].append('package.json')
        
        # Check for frameworks
        try:
            with open(path / 'package.json') as f:
                package_data = json.load(f)
                deps = {**package_data.get('dependencies', {}), 
                       **package_data.get('devDependencies', {})}
                
                if 'react' in deps:
                    info['frameworks'].append('React')
                if 'vue' in deps:
                    info['frameworks'].append('Vue')
                if 'angular' in deps or '@angular/core' in deps:
                    info['frameworks'].append('Angular')
                if 'express' in deps:
                    info['frameworks'].append('Express')
                if 'next' in deps:
                    info['frameworks'].append('Next.js')
        except:
            pass
    
    if (path / 'requirements.txt').exists() or (path / 'pyproject.toml').exists():
        info['languages'].append('Python')
        if (path / 'requirements.txt').exists():
            info['config_files'].append('requirements.txt')
        if (path / 'pyproject.toml').exists():
            info['config_files'].append('pyproject.toml')
            
        # Check for frameworks
        if (path / 'manage.py').exists():
            info['frameworks'].append('Django')
        if any((path / 'app').glob('*.py')) or (path / 'app.py').exists():
            info['frameworks'].append('Flask or FastAPI')
    
    if (path / 'go.mod').exists():
        info['languages'].append('Go')
        info['config_files'].append('go.mod')
    
    if (path / 'pom.xml').exists():
        info['languages'].append('Java')
        info['config_files'].append('pom.xml')
    
    if any(path.glob('*.csproj')):
        info['languages'].append('.NET')
        info['config_files'].extend([f.name for f in path.glob('*.csproj')])
    
    if (path / 'Gemfile').exists():
        info['languages'].append('Ruby')
        info['config_files'].append('Gemfile')
    
    # Check for existing Docker files
    if (path / 'Dockerfile').exists():
        info['config_files'].append('Dockerfile')
    if (path / 'docker-compose.yml').exists() or (path / 'docker-compose.yaml').exists():
        info['config_files'].append('docker-compose.yml')
    
    return info


def suggest_services(project_info: Dict) -> List[str]:
    """
    Suggest services based on project type
    
    Returns:
        list: Suggested services
    """
    services = []
    
    # Web frameworks usually need a database
    web_frameworks = ['Django', 'Flask or FastAPI', 'Express', 'React', 'Vue', 'Angular']
    if any(fw in project_info['frameworks'] for fw in web_frameworks):
        services.append('PostgreSQL or MySQL')
        services.append('Redis (for caching)')
    
    # Python projects might need Redis
    if 'Python' in project_info['languages']:
        if 'Redis' not in services:
            services.append('Redis (optional)')
    
    return services


def generate_port_suggestions(num_services: int) -> Dict[str, int]:
    """
    Generate port suggestions for services
    
    Returns:
        dict: Service name to port mapping
    """
    base_ports = {
        'frontend': 3000,
        'api': 8000,
        'backend': 8000,
        'postgres': 5432,
        'mysql': 3306,
        'mongodb': 27017,
        'redis': 6379,
        'rabbitmq': 5672,
        'rabbitmq-management': 15672,
        'elasticsearch': 9200,
        'kibana': 5601
    }
    
    return base_ports


def main():
    """
    Main function for interactive environment generation
    """
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = os.getcwd()
    
    print(f"Analyzing project at: {project_path}")
    print("=" * 60)
    
    project_info = detect_project_type(project_path)
    
    print("\nDetected Project Information:")
    print(f"  Languages: {', '.join(project_info['languages']) or 'None detected'}")
    print(f"  Frameworks: {', '.join(project_info['frameworks']) or 'None detected'}")
    print(f"  Config Files: {', '.join(project_info['config_files']) or 'None detected'}")
    
    suggested_services = suggest_services(project_info)
    if suggested_services:
        print(f"\nSuggested Services:")
        for service in suggested_services:
            print(f"  - {service}")
    
    port_suggestions = generate_port_suggestions(5)
    print(f"\nSuggested Ports:")
    for service, port in port_suggestions.items():
        print(f"  {service}: {port}")
    
    print("\n" + "=" * 60)
    print("Use this information when running the generate-tilt-dev-environment skill")


if __name__ == '__main__':
    main()
