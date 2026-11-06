# Identity and tenant security setup

## Identity provider: Amazon Cognito

StarUB Hub uses **Amazon Cognito User Pools** as its OIDC identity provider. The API accepts Cognito **access tokens** only; do not send ID tokens to API endpoints.

### Required configuration

Create a Cognito User Pool in the deployment's AWS Region, then create a separate app client for the StarUB Hub web application.

Recommended web-client settings:
- Use the authorization code grant with PKCE (no client secret in a browser-based public client).
- Register exact development and production callback and sign-out URLs.
- Enable only the required OAuth scopes; add custom resource-server scopes when domain-level API scopes are introduced.
- Configure MFA according to the deployment's risk policy, plus account recovery and user lifecycle controls.
- Keep the app client ID public; never place AWS credentials or a client secret in frontend code.

Set these API environment variables from the selected User Pool and app client:

| Variable | Value |
|---|---|
| `AUTH_ISSUER` | `https://cognito-idp.<region>.amazonaws.com/<user-pool-id>` |
| `AUTH_CLIENT_ID` | The web app client's ID; the API rejects tokens issued to another app client |
| `AUTH_JWKS_URL` | `<AUTH_ISSUER>/.well-known/jwks.json` |
| `AUTH_AUDIENCE` | Optional; set only if Cognito access tokens include and the API should enforce a resource-server `aud` claim |

The issuer must match Cognito's canonical issuer exactly (no extra trailing slash). The API fetches signing keys from the User Pool JWKS endpoint, pins the accepted algorithm to RS256, and validates signature, issuer, expiry, issued-at, subject, `client_id`, and `token_use=access`. Cognito's access-token `client_id` claim is checked against `AUTH_CLIENT_ID`; the ID-token `aud` claim is not used as a substitute. If a resource-server audience is configured, the API also validates it.

Do not configure `AUTH_AUDIENCE` with the app client ID for a standard Cognito access token unless the token actually contains that audience claim. Keep access-token lifetimes appropriately short and use Cognito's supported refresh-token rotation/lifecycle controls.

## Tenant selection

1. The client completes the Cognito authorization-code flow with PKCE and obtains an access token.
2. `GET /api/v1/tenants` lists active tenant memberships for the verified Cognito token subject (`sub`).
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
- `GET /api/v1/ready`: returns ready only when database and Cognito settings are configured and the database responds.
- `GET /api/v1/me`: verified token subject and optional profile claims.
- `GET /api/v1/tenants`: active memberships for the verified subject.
- `GET /api/v1/tenant-context`: requires `X-Tenant-ID` and verifies active membership before returning selected tenant and role.

## Configuration

Copy `apps/api/.env.example` to a local, untracked `.env` and replace every placeholder with the values from the deployed Cognito User Pool, app client, and database. `CORS_ORIGINS` must be a JSON array, for example `["http://localhost:3000"]`. Never commit AWS credentials, client secrets, signing keys, or database credentials.

The AWS account, Region, User Pool ID, app client ID, callback URLs, and production secrets have not yet been supplied or provisioned. Provider-specific code/configuration is now aligned to Cognito, but hosted sign-in is not live until those deployment values and the frontend OIDC flow are configured.
