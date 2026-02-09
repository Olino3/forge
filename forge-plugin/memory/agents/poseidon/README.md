# Poseidon Agent Memory

This directory stores project-specific knowledge for the `@poseidon` agent.

## Structure

```
poseidon/
├── pipelines/        # Track data pipeline architectures and patterns
├── transformations/  # Record data transformation logic and schemas
├── streams/          # Store stream processing configurations
└── integrations/     # Maintain data source and sink integrations
```

## Usage

The `@poseidon` agent automatically stores and retrieves:
- Pipeline architectures and data flows
- Transformation logic and business rules
- Schema mappings and conversions
- Data quality rules and validations
- Integration patterns and configurations
- Performance optimizations and tuning

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores pipeline designs and data patterns
3. **Retrieval**: Agent loads relevant data flows before building pipelines
4. **Updates**: Memory is updated as pipelines evolve
5. **Cleanup**: Deprecated pipelines can be archived with migration notes

## Example Memory Files

- `pipelines/customer-events-etl.md` - Customer events ETL pipeline design
- `transformations/order-schema-mapping.md` - Order data transformation logic
- `streams/kafka-event-processing.md` - Kafka stream processing configuration
- `integrations/salesforce-to-warehouse.md` - Salesforce data integration

## Best Practices

- Document schema evolution and versioning
- Record data quality rules and validation logic
- Store pipeline performance metrics and optimizations
- Track data lineage and dependencies
- Document integration authentication and configuration
- Keep transformation business rules up to date
- Review and update for schema changes
