# Security and privacy baseline

## Tenant isolation

- Resolve tenant context from an authenticated principal and verified tenant membership.
- Enforce tenant predicates in every tenant-owned query and mutation.
- Deny access by default; never treat a request header or body tenant ID as authorization.
- Add cross-tenant negative tests for every domain and file access path.
- Consider PostgreSQL row-level security as defense in depth, not a substitute for application authorization.

## Identity and authorization

- Use a managed OIDC/OAuth identity provider.
- Validate signature, issuer, audience, expiry, and authorized scopes/claims.
- Enforce tenant membership and role/permission checks server-side.
- Require MFA for privileged roles and sensitive workflows where supported.
- Use short-lived access tokens and secure refresh/session handling.

## Data protection

- TLS in transit and managed encryption at rest.
- Keep secrets in a secrets manager; never commit credentials.
- Store uploaded documents in private object storage with short-lived signed access.
- Validate file type, size, malware scan status, and authorization before access.
- Apply retention, deletion, export, and data-subject request workflows appropriate to the applicable legal basis and jurisdiction.

## Audit and sensitive operations

Record actor, tenant, action, target, timestamp, correlation ID, and relevant before/after metadata without logging secrets or unnecessary personal data.

AI must not independently make final admission decisions, sign contracts, transfer funds, change cap tables, disclose confidential information, or approve expenditure. Keep model/version, prompt/template version, input references, output, and human reviewer traceable.

## Release gates

- Threat model and privacy review
- Authorization and tenant-isolation tests
- Dependency and secret scanning
- Secure upload and access-control tests
- Backup/restore exercise
- Logging review for personal and confidential data
- Incident response and access-revocation procedures

This document is an engineering baseline, not legal advice or a claim of GDPR compliance. Obtain qualified review for actual processing activities, notices, retention schedules, contracts, and cross-border transfers.
