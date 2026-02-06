#!/bin/bash
# Schema Extraction Helper Script
# This script helps extract schema information from various file formats

set -euo pipefail

print_usage() {
    cat <<EOF
Usage: $0 [OPTIONS] <file-path>

Extract schema information from various file formats.

OPTIONS:
    -f, --format FORMAT    Specify format (json-schema, protobuf, graphql, openapi, avro, xsd)
    -o, --output FILE      Output file for extracted schema (default: stdout)
    -v, --validate         Validate schema syntax
    -h, --help             Show this help message

SUPPORTED FORMATS:
    - JSON Schema (.json, .schema.json)
    - Protocol Buffers (.proto)
    - GraphQL (.graphql, .gql)
    - OpenAPI (.yaml, .json)
    - Apache Avro (.avsc)
    - XML Schema (.xsd)

EXAMPLES:
    $0 schema/user.json
    $0 --format protobuf protos/service.proto
    $0 --validate api/openapi.yaml
    $0 --output extracted.txt schema.graphql

EOF
}

detect_format() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        proto)
            echo "protobuf"
            ;;
        graphql|gql)
            echo "graphql"
            ;;
        avsc)
            echo "avro"
            ;;
        xsd)
            echo "xsd"
            ;;
        json)
            if [[ "$file" == *.schema.json ]]; then
                echo "json-schema"
            elif grep -q '"openapi"' "$file" 2>/dev/null; then
                echo "openapi"
            elif grep -q '"type".*"record"' "$file" 2>/dev/null; then
                echo "avro"
            else
                echo "json-schema"
            fi
            ;;
        yaml|yml)
            if grep -q 'openapi:' "$file" 2>/dev/null; then
                echo "openapi"
            else
                echo "yaml"
            fi
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

extract_json_schema() {
    local file="$1"
    
    echo "=== JSON Schema Analysis ==="
    echo "File: $file"
    
    if command -v jq &> /dev/null; then
        echo ""
        echo "Schema Version:"
        jq -r '."$schema" // "Not specified"' "$file"
        
        echo ""
        echo "Title:"
        jq -r '.title // "Not specified"' "$file"
        
        echo ""
        echo "Properties:"
        jq -r '.properties | keys[]' "$file" 2>/dev/null || echo "No properties found"
        
        echo ""
        echo "Required Fields:"
        jq -r '.required[]' "$file" 2>/dev/null || echo "No required fields specified"
    else
        echo "jq not installed, showing raw content:"
        cat "$file"
    fi
}

extract_protobuf() {
    local file="$1"
    
    echo "=== Protocol Buffers Analysis ==="
    echo "File: $file"
    
    echo ""
    echo "Syntax:"
    grep -E '^syntax\s*=' "$file" || echo "Not specified"
    
    echo ""
    echo "Package:"
    grep -E '^package\s+' "$file" || echo "Not specified"
    
    echo ""
    echo "Imports:"
    grep -E '^import\s+' "$file" || echo "No imports"
    
    echo ""
    echo "Messages:"
    grep -E '^message\s+\w+' "$file" | sed 's/message /  - /' || echo "No messages"
    
    echo ""
    echo "Services:"
    grep -E '^service\s+\w+' "$file" | sed 's/service /  - /' || echo "No services"
    
    echo ""
    echo "Enums:"
    grep -E '^enum\s+\w+' "$file" | sed 's/enum /  - /' || echo "No enums"
}

extract_graphql() {
    local file="$1"
    
    echo "=== GraphQL Schema Analysis ==="
    echo "File: $file"
    
    echo ""
    echo "Types:"
    grep -E '^type\s+\w+' "$file" | sed 's/type /  - /' || echo "No types"
    
    echo ""
    echo "Interfaces:"
    grep -E '^interface\s+\w+' "$file" | sed 's/interface /  - /' || echo "No interfaces"
    
    echo ""
    echo "Enums:"
    grep -E '^enum\s+\w+' "$file" | sed 's/enum /  - /' || echo "No enums"
    
    echo ""
    echo "Inputs:"
    grep -E '^input\s+\w+' "$file" | sed 's/input /  - /' || echo "No inputs"
    
    echo ""
    echo "Queries:"
    grep -A 20 '^type Query' "$file" | grep -E '^\s+\w+' | sed 's/^/  - /' || echo "No queries"
    
    echo ""
    echo "Mutations:"
    grep -A 20 '^type Mutation' "$file" | grep -E '^\s+\w+' | sed 's/^/  - /' || echo "No mutations"
}

extract_openapi() {
    local file="$1"
    
    echo "=== OpenAPI Schema Analysis ==="
    echo "File: $file"
    
    if command -v yq &> /dev/null || command -v jq &> /dev/null; then
        local tool
        if command -v yq &> /dev/null; then
            tool="yq"
        else
            tool="jq"
        fi
        
        echo ""
        echo "OpenAPI Version:"
        $tool -r '.openapi' "$file" 2>/dev/null || echo "Not specified"
        
        echo ""
        echo "Info:"
        $tool -r '.info.title' "$file" 2>/dev/null || echo "Not specified"
        $tool -r '.info.version' "$file" 2>/dev/null || echo "Version not specified"
        
        echo ""
        echo "Schemas:"
        $tool -r '.components.schemas | keys[]' "$file" 2>/dev/null || echo "No schemas found"
        
        echo ""
        echo "Paths:"
        $tool -r '.paths | keys[]' "$file" 2>/dev/null || echo "No paths found"
    else
        echo "yq or jq not installed, showing raw content"
        cat "$file"
    fi
}

validate_schema() {
    local file="$1"
    local format="$2"
    
    echo "=== Schema Validation ==="
    
    case "$format" in
        json-schema)
            if command -v ajv &> /dev/null; then
                ajv compile -s "$file"
            else
                echo "ajv not installed, skipping validation"
            fi
            ;;
        protobuf)
            if command -v protoc &> /dev/null; then
                protoc --descriptor_set_out=/dev/null "$file"
            else
                echo "protoc not installed, skipping validation"
            fi
            ;;
        graphql)
            if command -v graphql-schema-linter &> /dev/null; then
                graphql-schema-linter "$file"
            else
                echo "graphql-schema-linter not installed, skipping validation"
            fi
            ;;
        *)
            echo "Validation not supported for format: $format"
            ;;
    esac
}

# Parse arguments
FORMAT=""
OUTPUT=""
VALIDATE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -v|--validate)
            VALIDATE=true
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            FILE="$1"
            shift
            ;;
    esac
done

# Check if file is provided
if [ -z "${FILE:-}" ]; then
    echo "Error: No file specified"
    print_usage
    exit 1
fi

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi

# Detect format if not specified
if [ -z "$FORMAT" ]; then
    FORMAT=$(detect_format "$FILE")
    echo "Detected format: $FORMAT"
    echo ""
fi

# Extract schema based on format
extract_func() {
    case "$FORMAT" in
        json-schema)
            extract_json_schema "$FILE"
            ;;
        protobuf)
            extract_protobuf "$FILE"
            ;;
        graphql)
            extract_graphql "$FILE"
            ;;
        openapi)
            extract_openapi "$FILE"
            ;;
        avro)
            extract_json_schema "$FILE"  # Avro schemas are JSON
            ;;
        *)
            echo "Unsupported format: $FORMAT"
            echo "Showing raw content:"
            cat "$FILE"
            ;;
    esac
}

# Output to file or stdout
if [ -n "$OUTPUT" ]; then
    extract_func > "$OUTPUT"
    echo "Schema information written to: $OUTPUT"
else
    extract_func
fi

# Validate if requested
if [ "$VALIDATE" = true ]; then
    echo ""
    validate_schema "$FILE" "$FORMAT"
fi
