# Implementation status — secure foundation increment

## Added in `develop`

- Next.js/React/TypeScript responsive workspace shell representing all 12 domains.
- FastAPI service with liveness and dependency-aware readiness endpoints.
- Amazon Cognito User Pools selected as the OIDC identity provider; AWS Region selected as `eu-west-1` (Europe/Ireland).
- Cognito access-token verification using User Pool JWKS, RS256 signature validation, exact issuer, expiry, issued-at, subject, app-client `client_id`, and `token_use=access` checks.
- Optional resource-server audience validation when Cognito tokens contain an `aud` claim and `AUTH_AUDIENCE` is configured.
- Verified-subject tenant membership lookup; client-selected tenant IDs are checked against active memberships.
- Transaction-local PostgreSQL tenant context and row-level security policies for entrepreneurs, projects, their relationship table, startups, and audit events.
- Core schema for tenants, memberships, entrepreneurs, projects, startups, and audit events.
- Cognito environment template, User Pool/app-client setup guide, and initial fail-closed authentication tests.

## Still outstanding

- Create the Cognito User Pool and public web app client in `eu-west-1`; provide User Pool ID, app client ID, hosted UI domain, exact callback/sign-out URLs, and MFA policy.
- Frontend Cognito Authorization Code + PKCE integration scaffold: sign-in redirect, callback handling, logout redirect, sessionStorage-backed OIDC state, access-token API helper, and silent-renew handling. Live Cognito sign-in remains unverified until a User Pool and app client exist.
- Configure frontend NEXT_PUBLIC_COGNITO_ISSUER, NEXT_PUBLIC_COGNITO_CLIENT_ID, NEXT_PUBLIC_COGNITO_DOMAIN, NEXT_PUBLIC_APP_URL, and API base URL; configure matching API issuer/client/JWKS settings and exact CORS origins.
- Create separate migration-owner and least-privilege runtime PostgreSQL roles and grant audited table privileges.
- Run migrations against PostgreSQL and verify RLS with the real runtime role, including cross-tenant negative tests.
- Add role/permission matrix and enforce it for each domain command.
- Verify Cognito refresh-token behavior and rotation in the target User Pool; add token revocation strategy, rate limiting, security headers, and production CORS origins. Browser OIDC tokens are currently held in sessionStorage, so XSS prevention remains a release requirement.
- Add tenant-scoped repositories and CRM/admissions endpoints, secure document storage, CI, integration tests, observability, backups, and deployment.

## Security caveat

This is a meaningful security foundation, not a production security certification. No Cognito User Pool or database credentials have been supplied, and no database migration, live Cognito token verification, integration test, or deployment has been executed. Do not expose business-data endpoints or store real tenant data until the Cognito configuration, deployment role grants, RLS behavior, and cross-tenant tests have been verified.
