from functools import lru_cache
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from app.settings import get_settings

bearer_scheme = HTTPBearer(auto_error=False, scheme_name='Cognito Access Token')


@lru_cache(maxsize=4)
def _jwks_client(jwks_url: str) -> PyJWKClient:
    # Cognito publishes rotating RS256 signing keys through the user-pool JWKS endpoint.
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
            algorithms=['RS256'],
            issuer=settings.auth_issuer,
            audience=settings.auth_audience,
            options={
                'require': ['exp', 'iat', 'sub', 'iss', 'client_id', 'token_use'],
                'verify_aud': bool(settings.auth_audience),
            },
            leeway=30,
        )
        # Cognito access tokens identify the app client with client_id (not the
        # ID-token aud claim) and distinguish themselves with token_use=access.
        if claims.get('client_id') != settings.auth_client_id:
            raise jwt.InvalidTokenError('Unexpected Cognito app client')
        if claims.get('token_use') != 'access':
            raise jwt.InvalidTokenError('Expected a Cognito access token')
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
