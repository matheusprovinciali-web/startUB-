from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg.rows import dict_row

from app.database import close_pool, database_ready, get_pool, open_pool
from app.security import current_principal
from app.settings import get_settings
from app.tenancy import TenantContext, tenant_context


@asynccontextmanager
async def lifespan(app: FastAPI):
    open_pool()
    yield
    close_pool()


settings = get_settings()
app = FastAPI(
    title='StarUB Hub API',
    version='0.2.0',
    openapi_url='/api/v1/openapi.json',
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'PATCH', 'DELETE'],
    allow_headers=['Authorization', 'Content-Type', 'Idempotency-Key', 'X-Tenant-ID'],
)


@app.get('/health', tags=['operations'])
def health():
    return {'status': 'ok', 'service': 'starub-api'}


@app.get('/api/v1/ready', tags=['operations'])
def ready():
    db_ok = database_ready()
    auth_ok = get_settings().auth_configured
    if not db_ok or not auth_ok:
        raise HTTPException(status_code=503, detail={
            'status': 'not_ready',
            'checks': {'database': 'ok' if db_ok else 'not_ready', 'identity': 'configured' if auth_ok else 'not_configured'},
        })
    return {'status': 'ready', 'checks': {'database': 'ok', 'identity': 'configured'}}


@app.get('/api/v1/me', tags=['identity'])
def me(principal: dict = Depends(current_principal)):
    # Return only stable, non-secret identity claims required by the client.
    return {
        'subject': principal['sub'],
        'email': principal.get('email'),
        'name': principal.get('name'),
    }


@app.get('/api/v1/tenants', tags=['tenancy'])
def list_my_tenants(principal: dict = Depends(current_principal)):
    pool = get_pool()
    with pool.connection() as conn:
        conn.row_factory = dict_row
        rows = conn.execute(
            """SELECT t.id, t.name, t.slug, m.role
               FROM tenant_memberships AS m
               JOIN tenants AS t ON t.id = m.tenant_id
               WHERE m.identity_subject = %s AND m.status = 'active'
               ORDER BY t.name""",
            (principal['sub'],),
        ).fetchall()
    return {'items': rows}


@app.get('/api/v1/tenant-context', tags=['tenancy'])
def get_tenant_context(context: TenantContext = Depends(tenant_context)):
    return {
        'tenant_id': str(context.tenant_id),
        'tenant_name': context.tenant_name,
        'role': context.role,
    }
