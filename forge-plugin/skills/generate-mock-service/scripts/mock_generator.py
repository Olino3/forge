#!/usr/bin/env python3
"""
Mock Service Generator Helper Script
Assists with generating mock service configurations and data
"""

import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any
from faker import Faker

fake = Faker()


def parse_openapi_spec(spec_path: str) -> Dict[str, Any]:
    """
    Parse OpenAPI specification to extract endpoints and schemas
    
    Args:
        spec_path: Path to OpenAPI spec file (JSON or YAML)
    
    Returns:
        dict: Parsed specification with endpoints and schemas
    """
    path = Path(spec_path)
    
    if not path.exists():
        raise FileNotFoundError(f"OpenAPI spec not found: {spec_path}")
    
    with open(path) as f:
        if path.suffix in ['.yaml', '.yml']:
            spec = yaml.safe_load(f)
        else:
            spec = json.load(f)
    
    endpoints = []
    
    # Extract endpoints
    for path_pattern, methods in spec.get('paths', {}).items():
        for method, details in methods.items():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                endpoints.append({
                    'path': path_pattern,
                    'method': method.upper(),
                    'summary': details.get('summary', ''),
                    'parameters': details.get('parameters', []),
                    'responses': details.get('responses', {})
                })
    
    return {
        'title': spec.get('info', {}).get('title', 'API'),
        'version': spec.get('info', {}).get('version', '1.0.0'),
        'endpoints': endpoints,
        'schemas': spec.get('components', {}).get('schemas', {})
    }


def generate_mock_data(schema: Dict[str, Any], count: int = 10) -> List[Dict[str, Any]]:
    """
    Generate realistic mock data based on a schema
    
    Args:
        schema: JSON schema definition
        count: Number of items to generate
    
    Returns:
        list: Generated mock data items
    """
    data = []
    
    for i in range(count):
        item = generate_item_from_schema(schema, i)
        data.append(item)
    
    return data


def generate_item_from_schema(schema: Dict[str, Any], index: int = 0) -> Dict[str, Any]:
    """
    Generate a single item from a JSON schema
    
    Args:
        schema: JSON schema definition
        index: Item index for deterministic data
    
    Returns:
        dict: Generated item
    """
    Faker.seed(index)
    
    item = {}
    properties = schema.get('properties', {})
    
    for prop_name, prop_schema in properties.items():
        prop_type = prop_schema.get('type', 'string')
        prop_format = prop_schema.get('format', '')
        
        # Generate data based on type
        if prop_type == 'string':
            if prop_format == 'email':
                item[prop_name] = fake.email()
            elif prop_format == 'date-time':
                item[prop_name] = fake.iso8601()
            elif prop_format == 'date':
                item[prop_name] = fake.date()
            elif prop_format == 'uuid':
                item[prop_name] = str(fake.uuid4())
            elif 'name' in prop_name.lower():
                item[prop_name] = fake.name()
            elif 'address' in prop_name.lower():
                item[prop_name] = fake.address()
            elif 'phone' in prop_name.lower():
                item[prop_name] = fake.phone_number()
            elif 'url' in prop_name.lower():
                item[prop_name] = fake.url()
            else:
                item[prop_name] = fake.sentence()
        
        elif prop_type == 'integer':
            item[prop_name] = fake.random_int(min=1, max=1000)
        
        elif prop_type == 'number':
            item[prop_name] = round(fake.random.uniform(0, 1000), 2)
        
        elif prop_type == 'boolean':
            item[prop_name] = fake.boolean()
        
        elif prop_type == 'array':
            items_schema = prop_schema.get('items', {})
            item[prop_name] = [
                generate_item_from_schema(items_schema, i)
                for i in range(fake.random_int(min=0, max=5))
            ]
        
        elif prop_type == 'object':
            item[prop_name] = generate_item_from_schema(prop_schema, index)
    
    return item


def suggest_endpoints(service_name: str) -> List[Dict[str, str]]:
    """
    Suggest common REST endpoints based on service name
    
    Args:
        service_name: Name of the service
    
    Returns:
        list: Suggested endpoints
    """
    # Extract resource name from service name
    resource = service_name.lower().replace('-service', '').replace('_service', '')
    if not resource.endswith('s'):
        resource += 's'
    
    return [
        {
            'path': f'/api/{resource}',
            'method': 'GET',
            'description': f'List all {resource}'
        },
        {
            'path': f'/api/{resource}/{{id}}',
            'method': 'GET',
            'description': f'Get {resource[:-1]} by ID'
        },
        {
            'path': f'/api/{resource}',
            'method': 'POST',
            'description': f'Create new {resource[:-1]}'
        },
        {
            'path': f'/api/{resource}/{{id}}',
            'method': 'PUT',
            'description': f'Update {resource[:-1]}'
        },
        {
            'path': f'/api/{resource}/{{id}}',
            'method': 'DELETE',
            'description': f'Delete {resource[:-1]}'
        }
    ]


def detect_auth_type(headers: Dict[str, str]) -> str:
    """
    Detect authentication type from headers
    
    Args:
        headers: Request headers
    
    Returns:
        str: Authentication type
    """
    if 'Authorization' in headers:
        if headers['Authorization'].startswith('Bearer '):
            return 'OAuth2/JWT'
        elif headers['Authorization'].startswith('Basic '):
            return 'Basic Auth'
    
    if 'X-API-Key' in headers or 'API-Key' in headers:
        return 'API Key'
    
    return 'None'


def main():
    """
    Main function for interactive mock generation assistance
    """
    print("Mock Service Generator Helper")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Parse OpenAPI spec if provided
        spec_path = sys.argv[1]
        print(f"\nParsing OpenAPI spec: {spec_path}")
        
        try:
            spec_info = parse_openapi_spec(spec_path)
            
            print(f"\nAPI: {spec_info['title']} v{spec_info['version']}")
            print(f"\nEndpoints found: {len(spec_info['endpoints'])}")
            
            for endpoint in spec_info['endpoints']:
                print(f"  {endpoint['method']:6} {endpoint['path']}")
                if endpoint['summary']:
                    print(f"         {endpoint['summary']}")
            
            print(f"\nSchemas found: {len(spec_info['schemas'])}")
            for schema_name in spec_info['schemas'].keys():
                print(f"  - {schema_name}")
            
            # Generate sample data for first schema
            if spec_info['schemas']:
                first_schema = list(spec_info['schemas'].values())[0]
                print("\nSample generated data:")
                sample_data = generate_mock_data(first_schema, count=2)
                print(json.dumps(sample_data, indent=2))
        
        except Exception as e:
            print(f"Error parsing spec: {e}")
            sys.exit(1)
    
    else:
        # Interactive mode
        service_name = input("\nEnter service name (e.g., payment-service): ")
        
        suggested_endpoints = suggest_endpoints(service_name)
        
        print(f"\nSuggested endpoints for '{service_name}':")
        for endpoint in suggested_endpoints:
            print(f"  {endpoint['method']:6} {endpoint['path']}")
            print(f"         {endpoint['description']}")
        
        print("\nRecommended mock server types:")
        print("  1. Express.js - Good for JavaScript/TypeScript projects")
        print("  2. Flask - Simple Python REST API mocks")
        print("  3. FastAPI - Modern Python with automatic docs")
        print("  4. WireMock - Configuration-based, no code needed")
        print("  5. Prism - Best if you have OpenAPI spec")
    
    print("\n" + "=" * 60)
    print("Use this information when running the generate-mock-service skill")


if __name__ == '__main__':
    main()
