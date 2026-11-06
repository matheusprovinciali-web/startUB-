# Architecture

## Product boundaries

The platform is a multi-tenant operating system for innovation hubs. Core domains:

1. Entrepreneur CRM and admissions
2. Facilities and hub management
3. Programs and project management
4. Startup development and incubation
5. Events and community
6. International relations and partnerships
7. Credits and rewards
8. Investors and investment relations
9. Mentors, experts and service providers
10. Documents, contracts and compliance
11. Analytics and reporting
12. Platform administration and AI intelligence

## Domain model invariants

- Entrepreneur, project, and startup are separate entities.
- Entrepreneurs and projects have a many-to-many relationship.
- A project may transition into a startup without erasing its project history.
- Startups and programs have a many-to-many relationship.
- Tenant-owned records carry an explicit tenant scope.
- Sensitive state changes are auditable.

## Application structure

Start with a modular monolith. Keep domain modules isolated behind service and repository boundaries; extract services only when scale, ownership, or operational needs justify it.

Suggested top-level layout: apps/web (Next.js), apps/api (FastAPI), packages/contracts (shared schemas), database (migrations and seeds), infra (deployment), docs (specifications).

## Initial vertical slice

1. Configuration, health checks, database connectivity, migrations
2. Identity integration and tenant membership/authorization
3. Tenant-aware audit trail
4. Entrepreneur and project records and their relationship
5. Public admissions intake with private document handling
6. Human review workflow with explainable AI assistance

## API conventions

- Prefix: /api/v1
- JSON REST endpoints with OpenAPI documentation
- Bounded pagination, validated filters, deterministic sorting
- Idempotency keys for sensitive create/command operations
- Consistent error envelope and request correlation ID
- Tenant scope derived from verified identity and membership, never a client-supplied tenant header
