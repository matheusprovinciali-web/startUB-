-- Apply after 001_core.sql. Run migrations with a dedicated schema owner.
-- The runtime API database role must NOT be a superuser, table owner, or BYPASSRLS role.
-- The API sets app.tenant_id transaction-locally only after checking active membership.

DO $$
DECLARE
  table_name TEXT;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'entrepreneurs', 'projects', 'entrepreneur_projects', 'startups', 'audit_events'
  ] LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', table_name);
    EXECUTE format(
      'CREATE POLICY tenant_isolation ON %I USING (tenant_id = NULLIF(current_setting(''app.tenant_id'', true), '''')::uuid) WITH CHECK (tenant_id = NULLIF(current_setting(''app.tenant_id'', true), '''')::uuid)',
      table_name
    );
  END LOOP;
END $$;

-- tenant_memberships and tenants are intentionally queried by the authenticated
-- subject before tenant context is selected. Grant the runtime role only the
-- minimum SELECT privileges needed for that membership lookup; do not expose
-- these tables through generic CRUD endpoints.
