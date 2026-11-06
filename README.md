# StarUB Hub

A multi-tenant SaaS CRM and Innovation Hub Operating System for incubators, accelerators, startups, programs, facilities, investors, mentors, and ecosystem partners.

## Product foundation

StarUB Hub is designed around distinct **people (entrepreneurs)**, **projects**, and **startups**. An entrepreneur may participate in multiple projects; a project may have multiple entrepreneurs; a project can mature into a startup. Startups may participate in multiple programs.

## Architecture direction

- Frontend: Next.js, React, TypeScript
- API: Python, FastAPI
- Data: PostgreSQL with tenant-scoped records
- Initial architecture: modular monolith
- API prefix: `/api/v1`
- Security baseline: authenticated identity, tenant membership, role-based authorization, audit events, least privilege

## Development status

This repository is being initialized. The first development increment focuses on the secure platform foundation, admissions, and the entrepreneur/project CRM. This is not yet a production-ready or deployed service.

See [docs/architecture.md](docs/architecture.md), [docs/roadmap.md](docs/roadmap.md), and [docs/security.md](docs/security.md).
