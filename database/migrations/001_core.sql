-- Initial relational foundation. Apply with a migration runner in each environment.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  default_currency CHAR(3) NOT NULL DEFAULT 'EUR',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tenant_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  identity_subject TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('owner','admin','manager','reviewer','member','viewer')),
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','invited','suspended')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, identity_subject)
);
CREATE INDEX tenant_memberships_subject_idx ON tenant_memberships(identity_subject, status);

CREATE TABLE entrepreneurs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  email TEXT,
  phone TEXT,
  professional_profile TEXT,
  status TEXT NOT NULL DEFAULT 'lead' CHECK (status IN ('lead','applicant','active','alumni','inactive')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, id)
);
CREATE INDEX entrepreneurs_tenant_created_idx ON entrepreneurs(tenant_id, created_at DESC);

CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  summary TEXT,
  stage TEXT NOT NULL DEFAULT 'idea' CHECK (stage IN ('idea','validation','development','launch','graduated','archived')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, id)
);
CREATE INDEX projects_tenant_created_idx ON projects(tenant_id, created_at DESC);

CREATE TABLE entrepreneur_projects (
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  entrepreneur_id UUID NOT NULL,
  project_id UUID NOT NULL,
  relationship_role TEXT NOT NULL DEFAULT 'founder',
  joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, entrepreneur_id, project_id),
  FOREIGN KEY (tenant_id, entrepreneur_id) REFERENCES entrepreneurs(tenant_id, id) ON DELETE CASCADE,
  FOREIGN KEY (tenant_id, project_id) REFERENCES projects(tenant_id, id) ON DELETE CASCADE
);

CREATE TABLE startups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  project_id UUID,
  legal_name TEXT,
  brand_name TEXT NOT NULL,
  trl SMALLINT CHECK (trl BETWEEN 1 AND 9),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, project_id) REFERENCES projects(tenant_id, id)
);

CREATE TABLE audit_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  actor_subject TEXT NOT NULL,
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID,
  request_id TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX audit_events_tenant_created_idx ON audit_events(tenant_id, created_at DESC);
