# StarUB Hub

A multi-tenant SaaS CRM and Innovation Hub Operating System for incubators, accelerators, startups, programs, facilities, investors, mentors, and ecosystem partners.

## Product foundation

StarUB Hub keeps **entrepreneurs**, **projects**, and **startups** as separate entities. Entrepreneurs may participate in multiple projects; projects may have multiple entrepreneurs; a project can mature into a startup without losing its history. Startups may participate in multiple programs.

## Architecture

- Frontend: Next.js, React, TypeScript (`apps/web`)
- API: Python, FastAPI (`apps/api`)
- Data: PostgreSQL (`database/migrations`)
- Identity: Amazon Cognito User Pools (OIDC), AWS Region `eu-west-1` (Europe/Ireland)
- Initial architecture: modular monolith
- API prefix: `/api/v1`

## Security-first development

The API foundation validates Amazon Cognito access tokens against the User Pool JWKS endpoint, enforces the configured app client ID and `token_use=access`, checks active tenant membership for every selected tenant, and sets transaction-local PostgreSQL RLS context. The runtime database role must be separate from the migration owner and must not bypass row-level security.

See [docs/identity-and-tenancy.md](docs/identity-and-tenancy.md) for Cognito User Pool and app-client setup. Copy [apps/api/.env.example](apps/api/.env.example) to an untracked local `.env` and replace all placeholders with your Cognito and database deployment values.

## Development status

This is an evolving development scaffold, not a deployed or production-ready service. Cognito and the AWS Region are selected, but the User Pool, app client, frontend sign-in flow, secrets, database roles, migrations, integration tests, and deployment must still be configured and verified before real data is processed. See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md), [docs/architecture.md](docs/architecture.md), [docs/roadmap.md](docs/roadmap.md), and [docs/security.md](docs/security.md).
