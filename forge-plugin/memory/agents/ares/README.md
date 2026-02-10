# Ares Agent Memory

This directory stores project-specific knowledge for the `@ares` agent.

## Structure

```
ares/
├── deployments/  # Track deployment configurations and outcomes
├── incidents/    # Record incidents and post-mortems
├── runbooks/     # Store operational procedures and playbooks
└── monitoring/   # Maintain monitoring and alerting configurations
```

## Usage

The `@ares` agent automatically stores and retrieves:
- Deployment procedures and checklists
- Incident reports and post-mortems
- Runbooks and playbooks
- Monitoring configurations and alert thresholds
- Disaster recovery procedures
- Performance baselines and optimizations

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Operations**: Agent stores deployment outcomes and incident learnings
3. **Retrieval**: Agent loads relevant runbooks and procedures before operations
4. **Updates**: Memory is updated after each deployment or incident
5. **Review**: Regular post-mortems update and refine procedures

## Example Memory Files

- `deployments/api-v2-rollout.md` - Deployment procedure and outcome
- `incidents/2026-02-01-database-outage.md` - Incident report and post-mortem
- `runbooks/database-failover.md` - Database failover procedure
- `monitoring/api-slo-alerts.md` - API monitoring and SLO alert configuration

## Best Practices

- Document all incidents with timeline and actions taken
- Keep runbooks up to date with current procedures
- Store both successful and failed deployment learnings
- Include metrics and outcomes for deployments
- Conduct blameless post-mortems
- Update procedures based on lessons learned
- Test runbooks regularly
