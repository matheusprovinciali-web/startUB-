from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app import security


def test_token_verification_fails_closed_without_oidc_configuration(monkeypatch):
    monkeypatch.setattr(
        security,
        'get_settings',
        lambda: SimpleNamespace(auth_configured=False),
    )
    with pytest.raises(HTTPException) as exc:
        security.verify_access_token('not-a-real-token')
    assert exc.value.status_code == 503


def test_current_principal_requires_bearer_credentials():
    with pytest.raises(HTTPException) as exc:
        security.current_principal(None)
    assert exc.value.status_code == 401
    assert exc.value.headers['WWW-Authenticate'] == 'Bearer'
