# Product roadmap

## Phase 0 — Foundation

- Repository conventions, local developer setup, CI checks
- PostgreSQL schema and migration discipline
- Identity provider integration
- Tenant membership, roles, permissions, and audit events
- Observability, secrets, backups, and environment configuration

## Phase 1 — Admissions and CRM

- Public admissions portal
- Entrepreneur, project, team, and application records
- Secure pitch-deck upload and version history
- Configurable evaluation rubric and human review
- Interview scheduling and decision tracking
- Onboarding checklist and two-year development plan

Initial evaluation rubric (configurable): problem 10%, solution/value 15%, market 15%, business model 15%, innovation 10%, validation 10%, team 10%, financial understanding 10%, scalability/impact 5%. AI may assist with evidence-based assessment; people make admission decisions.

## Phase 2 — Incubation and programs

- Startup profiles, teams, cap tables, TRL, roadmaps, legal and financial records
- 16 business-plan modules, fortnightly cadence over an indicative 32-week journey
- Revision and approval workflow; subsequent modules unlock after human approval
- Program calls, teams, tasks, dependencies, milestones, budgets, hours, KPIs, and evidence
- Multi-currency support with exchange-rate source and timestamp

## Phase 3 — Facilities and ecosystem

- Seat inventory and assignment history (initial reference configuration: 48 seats)
- Room and equipment reservations with conflict prevention
- Maintenance tickets, suppliers, and service-level tracking
- Events, registrations, community, partners, mentors, and service providers

## Phase 4 — Capital and intelligence

- Investor CRM, introductions, fundraising pipeline, and investment records
- Credits and rewards with immutable ledger semantics
- Analytics, operational reporting, and exports
- AI-supported document classification, matching, and report generation

## Release discipline

Every increment should include acceptance criteria, migrations, authorization tests, audit coverage, API documentation, and operator notes. Do not mark a feature complete based on scaffolding alone. Record decisions, owners, and dates only when confirmed.
