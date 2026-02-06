#!/bin/bash
# Database Schema Introspection Helper Script
# Extracts schema metadata from various database systems

set -euo pipefail

print_usage() {
    cat <<EOF
Usage: $0 [OPTIONS] <database-type>

Extract schema information from databases.

OPTIONS:
    -h, --host HOST        Database host (default: localhost)
    -p, --port PORT        Database port (default: varies by type)
    -u, --user USER        Database username
    -d, --database DB      Database name
    -o, --output FILE      Output file (default: stdout)
    -f, --format FORMAT    Output format (sql|json|md) (default: md)
    --help                 Show this help message

DATABASE TYPES:
    postgres, postgresql   PostgreSQL database
    mysql, mariadb         MySQL/MariaDB database
    mongodb, mongo         MongoDB database
    sqlite                 SQLite database file

EXAMPLES:
    $0 -h localhost -u user -d mydb postgres
    $0 --format json -o schema.json postgres
    $0 --database myapp mongodb

NOTES:
    - Password will be prompted securely (not via command line)
    - For SQLite, use -d to specify the database file path
    - MongoDB may require authentication database (--authenticationDatabase)

EOF
}

# Default values
HOST="localhost"
PORT=""
USER=""
DATABASE=""
OUTPUT=""
FORMAT="md"
DB_TYPE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--host)
            HOST="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -u|--user)
            USER="$2"
            shift 2
            ;;
        -d|--database)
            DATABASE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        --help)
            print_usage
            exit 0
            ;;
        postgres|postgresql|mysql|mariadb|mongodb|mongo|sqlite)
            DB_TYPE="$1"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Check database type
if [ -z "$DB_TYPE" ]; then
    echo "Error: Database type not specified"
    print_usage
    exit 1
fi

# Set default ports if not specified
if [ -z "$PORT" ]; then
    case "$DB_TYPE" in
        postgres|postgresql)
            PORT=5432
            ;;
        mysql|mariadb)
            PORT=3306
            ;;
        mongodb|mongo)
            PORT=27017
            ;;
        sqlite)
            PORT=""  # Not applicable
            ;;
    esac
fi

# Prompt for password if needed (not for SQLite)
if [ "$DB_TYPE" != "sqlite" ]; then
    echo -n "Password: "
    read -s PASSWORD
    echo ""
fi

# Introspect database
introspect_postgres() {
    local PGPASSWORD="$PASSWORD"
    export PGPASSWORD
    
    local CONN="psql -h $HOST -p $PORT -U $USER -d $DATABASE -t -A"
    
    echo "# PostgreSQL Schema Analysis"
    echo ""
    echo "## Database Information"
    echo "Database: $DATABASE"
    echo "Host: $HOST:$PORT"
    echo "User: $USER"
    echo ""
    
    echo "## Tables"
    $CONN -c "
        SELECT table_schema, table_name, 
               (SELECT COUNT(*) FROM information_schema.columns c 
                WHERE c.table_schema = t.table_schema AND c.table_name = t.table_name) as column_count
        FROM information_schema.tables t
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    " | while IFS='|' read -r schema table cols; do
        echo "- $schema.$table ($cols columns)"
    done
    
    echo ""
    echo "## Table Details"
    
    $CONN -c "
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    " | while IFS='|' read -r schema table; do
        echo ""
        echo "### $schema.$table"
        echo ""
        echo "Columns:"
        $CONN -c "
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = '$schema' AND table_name = '$table'
            ORDER BY ordinal_position;
        " | while IFS='|' read -r col type nullable default; do
            echo "- $col: $type, nullable=$nullable, default=$default"
        done
        
        echo ""
        echo "Constraints:"
        $CONN -c "
            SELECT constraint_name, constraint_type
            FROM information_schema.table_constraints
            WHERE table_schema = '$schema' AND table_name = '$table';
        " | while IFS='|' read -r name type; do
            echo "- $name ($type)"
        done
        
        echo ""
        echo "Indexes:"
        $CONN -c "
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = '$schema' AND tablename = '$table';
        " | while IFS='|' read -r name def; do
            echo "- $name: $def"
        done
    done
    
    unset PGPASSWORD
}

introspect_mysql() {
    local MYSQL_PWD="$PASSWORD"
    export MYSQL_PWD
    
    local CONN="mysql -h $HOST -P $PORT -u $USER -D $DATABASE -s -N"
    
    echo "# MySQL Schema Analysis"
    echo ""
    echo "## Database Information"
    echo "Database: $DATABASE"
    echo "Host: $HOST:$PORT"
    echo "User: $USER"
    echo ""
    
    echo "## Tables"
    $CONN -e "SHOW TABLES;" | while read -r table; do
        local row_count=$($CONN -e "SELECT COUNT(*) FROM \`$table\`;" 2>/dev/null || echo "N/A")
        echo "- $table (rows: $row_count)"
    done
    
    echo ""
    echo "## Table Details"
    
    $CONN -e "SHOW TABLES;" | while read -r table; do
        echo ""
        echo "### $table"
        echo ""
        echo "Columns:"
        $CONN -e "DESCRIBE \`$table\`;" | while read -r field type null key default extra; do
            echo "- $field: $type, null=$null, key=$key, default=$default, extra=$extra"
        done
        
        echo ""
        echo "Indexes:"
        $CONN -e "SHOW INDEX FROM \`$table\`;" | tail -n +2 | while read -r line; do
            echo "- $line"
        done
        
        echo ""
        echo "Create Statement:"
        echo '```sql'
        $CONN -e "SHOW CREATE TABLE \`$table\`\\G" | grep "Create Table:" -A 100 | tail -n +2
        echo '```'
    done
    
    unset MYSQL_PWD
}

introspect_mongodb() {
    echo "# MongoDB Schema Analysis"
    echo ""
    echo "## Database Information"
    echo "Database: $DATABASE"
    echo "Host: $HOST:$PORT"
    echo ""
    
    # MongoDB introspection requires mongosh or mongo shell
    if command -v mongosh &> /dev/null; then
        MONGO_CMD="mongosh"
    elif command -v mongo &> /dev/null; then
        MONGO_CMD="mongo"
    else
        echo "Error: mongosh or mongo command not found"
        exit 1
    fi
    
    local CONN_STRING="mongodb://$USER:$PASSWORD@$HOST:$PORT/$DATABASE"
    
    echo "## Collections"
    $MONGO_CMD "$CONN_STRING" --quiet --eval "
        db.getCollectionNames().forEach(function(collection) {
            var count = db[collection].count();
            print(collection + ' (' + count + ' documents)');
        });
    "
    
    echo ""
    echo "## Collection Schemas (Inferred from samples)"
    
    $MONGO_CMD "$CONN_STRING" --quiet --eval "
        db.getCollectionNames().forEach(function(collection) {
            print('');
            print('### ' + collection);
            print('');
            var sample = db[collection].findOne();
            if (sample) {
                printjson(sample);
            }
            print('');
            print('Indexes:');
            db[collection].getIndexes().forEach(function(index) {
                printjson(index);
            });
        });
    "
}

introspect_sqlite() {
    if [ -z "$DATABASE" ]; then
        echo "Error: Database file path required for SQLite"
        exit 1
    fi
    
    if [ ! -f "$DATABASE" ]; then
        echo "Error: Database file not found: $DATABASE"
        exit 1
    fi
    
    echo "# SQLite Schema Analysis"
    echo ""
    echo "## Database Information"
    echo "Database File: $DATABASE"
    echo ""
    
    echo "## Tables"
    sqlite3 "$DATABASE" "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;" | while read -r table; do
        local row_count=$(sqlite3 "$DATABASE" "SELECT COUNT(*) FROM \`$table\`;")
        echo "- $table (rows: $row_count)"
    done
    
    echo ""
    echo "## Table Details"
    
    sqlite3 "$DATABASE" "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;" | while read -r table; do
        echo ""
        echo "### $table"
        echo ""
        echo "Schema:"
        echo '```sql'
        sqlite3 "$DATABASE" "SELECT sql FROM sqlite_master WHERE type='table' AND name='$table';"
        echo '```'
        
        echo ""
        echo "Indexes:"
        sqlite3 "$DATABASE" "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='$table';" | while read -r index; do
            if [ -n "$index" ]; then
                echo "- $index"
            fi
        done
    done
}

# Execute introspection
introspect_func=""
case "$DB_TYPE" in
    postgres|postgresql)
        introspect_func="introspect_postgres"
        ;;
    mysql|mariadb)
        introspect_func="introspect_mysql"
        ;;
    mongodb|mongo)
        introspect_func="introspect_mongodb"
        ;;
    sqlite)
        introspect_func="introspect_sqlite"
        ;;
esac

# Output to file or stdout
if [ -n "$OUTPUT" ]; then
    $introspect_func > "$OUTPUT"
    echo "Schema information written to: $OUTPUT"
else
    $introspect_func
fi
