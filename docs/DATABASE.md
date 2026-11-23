# TraceWise Database Design

## Database

TraceWise uses PostgreSQL with SQLAlchemy 2.x and Alembic.

## Design conventions

- UUID primary keys.
- Timezone-aware timestamps.
- UTC timestamps supplied by PostgreSQL.
- Organization-scoped tenant data.
- JSON columns for flexible attributes and evidence payloads.
- Foreign keys and composite foreign keys for tenant-aware references.
- Indexes for common organization, service, incident, and time queries.

## Identity and tenancy

| Table | Purpose |
|---|---|
| organizations | Tenant accounts |
| users | User accounts |
| memberships | User-to-organization roles |

## Cloud resources

| Table | Purpose |
|---|---|
| environments | Development, staging, production |
| services | Applications and infrastructure services |
| api_keys | Hashed ingestion credentials |

API keys are stored as SHA-256 hashes. Raw API keys are never persisted.

## Telemetry

| Table | Purpose |
|---|---|
| logs | Structured application log events |
| metrics | Numeric time-series measurements |
| traces | Distributed tracing spans |
| service_dependencies | Relationships between services |

## Reliability intelligence

| Table | Purpose |
|---|---|
| anomalies | Detected unusual behavior |
| incidents | Grouped reliability events |
| evidence | Supporting observations for investigations |
| root_cause_candidates | Ranked possible causes |

## Tenant isolation

Tenant-owned records carry an organization ID.

Composite foreign keys protect references between tenant-owned resources, including:
- Services and environments.
- API keys and environments.
- Telemetry and services/environments.
- Dependencies and services.
- Incidents and environments.
- Evidence and incidents.
- Root-cause candidates and incidents/services.

Application queries must still filter by the authenticated organization.
Database constraints complement, but do not replace, authorization checks.

## Future extensions

The current schema is an MVP foundation. Future migrations may add:
- Telemetry retention and partitioning.
- Metric aggregation and rollups.
- Incident-to-anomaly association.
- Alert policies and notification history.
- Audit logs.
- Organization-level usage and billing.
- More detailed trace relationships.