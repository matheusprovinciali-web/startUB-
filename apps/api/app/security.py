from functools import lru_cache
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from app.settings import get_settings

bearer_scheme = HTTPBearer(auto_error=False, scheme_name='OIDC Bearer Token')


@lru_cache(maxsize=4)
def _jwks_client(jwks_url: str) -> PyJWKClient:
    # PyJWT caches JWKS keys and refreshes when an unknown key ID is encountered.
    return PyJWKClient(jwks_url, cache_jwk_set=True, lifespan=300, timeout=5)


def verify_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.auth_configured:
        raise HTTPException(status_code=503, detail='Identity provider is not configured')
    try:
        signing_key = _jwks_client(settings.auth_jwks_url).get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256', 'ES256'],
            audience=settings.auth_audience,
            issuer=settings.auth_issuer,
            options={'require': ['exp', 'iat', 'sub', 'iss', 'aud']},
            leeway=30,
        )
        if not isinstance(claims.get('sub'), str) or not claims['sub'].strip():
            raise jwt.InvalidTokenError('Missing subject')
        return claims
    except Exception as exc:
        # Do not leak signature, key lookup, or claim-validation details to clients.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired access token',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from exc


def current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    if credentials is None or credentials.scheme.lower() != 'bearer':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bearer access token required',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return verify_access_token(credentials.credentials)
