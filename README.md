# StarUB Hub

A multi-tenant SaaS CRM and Innovation Hub Operating System for incubators, accelerators, startups, programs, facilities, investors, mentors, and ecosystem partners.

## Product foundation

StarUB Hub keeps **entrepreneurs**, **projects**, and **startups** as separate entities. Entrepreneurs may participate in multiple projects; projects may have multiple entrepreneurs; a project can mature into a startup without losing its history. Startups may participate in multiple programs.

## Architecture

- Frontend: Next.js, React, TypeScript (`apps/web`)
- API: Python, FastAPI (`apps/api`)
- Data: PostgreSQL (`database/migrations`)
- Initial architecture: modular monolith
- API prefix: `/api/v1`

## Security-first development

The API foundation validates OIDC access tokens against a configured JWKS endpoint, checks active tenant membership for every selected tenant, and sets transaction-local PostgreSQL RLS context. The runtime database role must be separate from the migration owner and must not bypass row-level security.

See [docs/identity-and-tenancy.md](docs/identity-and-tenancy.md) before configuring local or hosted environments. Copy `apps/api/.env.example` to an untracked local `.env` and supply values from the chosen identity provider and database environment.

## Development status

This is an evolving development scaffold, not a deployed or production-ready service. The actual identity provider, secrets, database roles, migrations, integration tests, and deployment must be configured and verified before real data is processed. See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md), [docs/architecture.md](docs/architecture.md), [docs/roadmap.md](docs/roadmap.md), and [docs/security.md](docs/security.md).
