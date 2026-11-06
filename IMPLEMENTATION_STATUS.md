# Implementation status — secure foundation increment

## Added in `develop`

- Next.js/React/TypeScript responsive workspace shell representing all 12 domains.
- FastAPI service with liveness and dependency-aware readiness endpoints.
- OIDC access-token verification using provider JWKS, pinned RS256/ES256 algorithms, and issuer/audience/expiry/issued-at/subject validation.
- Verified-subject tenant membership lookup; client-selected tenant IDs are checked against active memberships.
- Transaction-local PostgreSQL tenant context and row-level security policies for entrepreneurs, projects, their relationship table, startups, and audit events.
- Core schema for tenants, memberships, entrepreneurs, projects, startups, and audit events.
- Environment template, identity/tenant deployment guidance, and initial fail-closed authentication tests.

## Still outstanding

- Select and configure the actual OIDC provider, register web/API clients, configure callback/logout URLs, MFA, and provision production secrets.
- Create separate migration-owner and least-privilege runtime PostgreSQL roles and grant audited table privileges.
- Run migrations against PostgreSQL and verify RLS with the real runtime role, including cross-tenant negative tests.
- Add role/permission matrix and enforce it for each domain command.
- Add token lifecycle/revocation strategy, rate limiting, CSRF/session decisions for browser integration, security headers, and production CORS origins.
- Add tenant-scoped repositories and CRM/admissions endpoints, secure document storage, CI, integration tests, observability, backups, and deployment.

## Security caveat

This is a meaningful security foundation, not a production security certification. No identity provider or database credentials have been supplied, and no database migration, live token verification, integration test, or deployment has been executed. Do not expose business-data endpoints or store real tenant data until the deployment role grants, RLS behavior, identity-provider configuration, and cross-tenant tests have been verified.
