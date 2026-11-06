from collections.abc import Generator
from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from psycopg.rows import dict_row

from app.database import get_pool
from app.security import current_principal


@dataclass(frozen=True)
class TenantContext:
    tenant_id: UUID
    tenant_name: str
    role: str
    subject: str
    connection: object


def tenant_context(
    tenant_id: UUID = Header(alias='X-Tenant-ID'),
    principal: dict = Depends(current_principal),
) -> Generator[TenantContext, None, None]:
    """Select a tenant only after verifying active membership for the JWT subject.

    X-Tenant-ID is a selector, never an authorization credential. RLS context is
    transaction-local and disappears when the request transaction ends.
    """
    subject = principal['sub']
    pool = get_pool()
    with pool.connection() as conn:
        with conn.transaction():
            conn.row_factory = dict_row
            membership = conn.execute(
                """SELECT t.id, t.name, m.role
                   FROM tenant_memberships AS m
                   JOIN tenants AS t ON t.id = m.tenant_id
                   WHERE m.identity_subject = %s
                     AND m.tenant_id = %s
                     AND m.status = 'active'""",
                (subject, tenant_id),
            ).fetchone()
            if membership is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='No active membership for the selected tenant',
                )
            conn.execute("SELECT set_config('app.tenant_id', %s, true)", (str(tenant_id),))
            yield TenantContext(
                tenant_id=membership['id'],
                tenant_name=membership['name'],
                role=membership['role'],
                subject=subject,
                connection=conn,
            )


def require_roles(*allowed_roles: str):
    def dependency(context: TenantContext = Depends(tenant_context)) -> TenantContext:
        if context.role not in allowed_roles:
            raise HTTPException(status_code=403, detail='Insufficient tenant role')
        return context
    return dependency
