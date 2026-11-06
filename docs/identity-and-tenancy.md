# Identity and tenant security setup

## Identity provider: Amazon Cognito

StarUB Hub uses **Amazon Cognito User Pools** as its OIDC identity provider. The selected deployment Region is **Europe (Ireland), `eu-west-1`**. The API accepts Cognito **access tokens** only; do not send ID tokens to API endpoints.

### Required configuration

Create a Cognito User Pool in `eu-west-1`, then create a separate app client for the StarUB Hub web application.

Recommended web-client settings:
- Use the authorization code grant with PKCE (no client secret in a browser-based public client).
- Register exact development and production callback and sign-out URLs.
- Enable only the required OAuth scopes; add custom resource-server scopes when domain-level API scopes are introduced.
- Configure MFA according to the deployment's risk policy, plus account recovery and user lifecycle controls.
- Keep the app client ID public; never place AWS credentials or a client secret in frontend code.

Set these API environment variables from the selected User Pool and app client:

| Variable | Value |
|---|---|
| `AWS_REGION` | `eu-west-1` |
| `AUTH_ISSUER` | `https://cognito-idp.eu-west-1.amazonaws.com/<user-pool-id>` |
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

Copy `apps/api/.env.example` to a local, untracked `.env` and replace every placeholder with the values from the Cognito User Pool in `eu-west-1`, app client, and database. `CORS_ORIGINS` must be a JSON array, for example `["http://localhost:3000"]`. Never commit AWS credentials, client secrets, signing keys, or database credentials.

The AWS account, User Pool ID, app client ID, callback URLs, and production secrets have not yet been supplied or provisioned. Provider code/configuration and the Region are selected, but hosted sign-in is not live until those deployment values and the frontend OIDC flow are configured.

## Next.js frontend: Authorization Code + PKCE

The apps/web frontend uses oidc-client-ts as a browser-based public OIDC client. It does not use or require a Cognito app-client secret.

1. Create a Cognito app client with no client secret and enable the authorization code grant. PKCE (S256) is used by the OIDC client; do not enable implicit grant.
2. Configure the Cognito managed-login domain.
3. Add these exact callback URLs to the app client:
   - Local callback: http://localhost:3000/auth/callback
   - Local sign-out URL: http://localhost:3000/auth/signed-out
   - Add the corresponding exact HTTPS URLs for each deployed environment.
4. Enable the OIDC scopes openid, email, and profile. Do not add a client secret to frontend configuration.
5. Copy apps/web/.env.example to apps/web/.env.local and replace the placeholders. Set NEXT_PUBLIC_APP_URL to the exact frontend origin and NEXT_PUBLIC_API_BASE_URL to the FastAPI origin.
6. Add the frontend origin to the API's CORS_ORIGINS JSON array. Keep the production list restricted to the deployed frontend origins.
7. Install dependencies and start the web app from apps/web with npm install and npm run dev.

The frontend requests an authorization code, uses the library's S256 PKCE verifier/challenge and state handling, then processes the callback at /auth/callback. Access tokens are sent as Bearer tokens by apps/web/lib/api.ts; tenant selection, when needed, is sent separately as X-Tenant-ID. The API remains responsible for validating the Cognito access token and tenant membership.

OIDC user state and protocol transaction state are stored in sessionStorage, not localStorage, and are scoped to the browser tab. This is a browser SPA integration, not an HttpOnly server-side session. Any successful XSS could still access browser-held tokens: enforce a restrictive Content Security Policy, avoid unsafe HTML, keep dependencies patched, and complete a security review before production. The configured silent-renew path depends on Cognito issuing a refresh token and must be verified with the real app client and refresh-token rotation settings. If refresh fails, the UI returns to an unauthenticated state and the user must sign in again.

The current scaffold provides sign-in controls and a reusable authenticated API fetch helper; it does not yet gate every dashboard route or implement the tenant-selection UI. Do not treat the static dashboard shell as proof that a user is authenticated.