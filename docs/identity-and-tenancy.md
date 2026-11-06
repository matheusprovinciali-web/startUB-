# Identity and tenant security setup

## Identity provider contract

Configure an OIDC provider that issues signed access tokens for this API. Set `AUTH_ISSUER`, `AUTH_AUDIENCE`, and `AUTH_JWKS_URL` in the API runtime environment. The API validates the JWT signature against the provider JWKS, pins accepted algorithms to RS256/ES256, and validates issuer, audience, expiry, issued-at, and subject. The API does not accept unsigned tokens or trust identity/role/tenant values supplied in request bodies.

Use the provider's access-token audience for this API, not an ID token intended for the browser client. Keep the issuer exact, including its canonical trailing slash if the provider uses one. Configure token lifetime, MFA, user lifecycle, and recovery in the identity provider.

## Tenant selection

1. The client obtains a valid access token.
2. `GET /api/v1/tenants` lists active tenant memberships for the verified token subject.
3. The client selects one tenant and sends its UUID in `X-Tenant-ID`.
4. The API looks up an active membership for the verified subject and selected tenant. The header is only a selector and never grants access.
5. The API establishes a transaction-local `app.tenant_id` setting. PostgreSQL row-level security policies filter and constrain tenant-owned rows for that transaction.

Tenant roles currently defined in the core schema: owner, admin, manager, reviewer, member, viewer. Role-specific permissions must be applied to each command as domain endpoints are introduced. The helper `require_roles(...)` is available for that purpose; do not assume authentication alone implies authorization.

## Database deployment requirements

- Apply migrations with a dedicated schema-owner role.
- Run the API with a separate least-privilege database role.
- The API role must not be superuser, table owner, or have `BYPASSRLS`.
- Use [the example runtime-role grants](../database/roles/runtime_role.example.sql) as a starting point, replacing the database name and reviewing grants against the deployed schema.
- Provision the runtime role password separately through a secrets manager; never commit it.
- Use TLS for remote PostgreSQL connections and store `DATABASE_URL` in a secrets manager.
- Test cross-tenant reads and writes using the actual runtime database role before release.

## Current API endpoints

- `GET /health`: process liveness only; does not prove dependencies are ready.
- `GET /api/v1/ready`: returns ready only when database and OIDC settings are configured and the database responds.
- `GET /api/v1/me`: verified token subject and optional profile claims.
- `GET /api/v1/tenants`: active memberships for the verified subject.
- `GET /api/v1/tenant-context`: requires `X-Tenant-ID` and verifies active membership before returning selected tenant and role.

## Configuration

Copy `apps/api/.env.example` to a local, untracked `.env` and replace all placeholders. `CORS_ORIGINS` must be a JSON array, for example `["http://localhost:3000"]`. Never commit real issuer secrets, client secrets, signing keys, or database credentials. OIDC provider-specific client setup and production secret provisioning remain deployment tasks.
