-- Run as the database administrator after creating the database and applying schema migrations.
-- Provision the role password separately through your secrets manager; do not put it in source control.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'starub_api') THEN
    CREATE ROLE starub_api LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
  END IF;
END $$;

-- Replace starub_database with the actual database name before execution.
GRANT CONNECT ON DATABASE starub_database TO starub_api;
GRANT USAGE ON SCHEMA public TO starub_api;
GRANT SELECT ON tenants, tenant_memberships TO starub_api;
GRANT SELECT, INSERT, UPDATE, DELETE ON entrepreneurs, projects, entrepreneur_projects, startups TO starub_api;
GRANT SELECT, INSERT ON audit_events TO starub_api;

-- Do not grant ownership, BYPASSRLS, TRUNCATE, REFERENCES, or schema CREATE to the runtime role.
-- Re-run and review grants whenever new tenant-owned tables are introduced.
