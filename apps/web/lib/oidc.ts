'use client';

import { UserManager, WebStorageStateStore } from 'oidc-client-ts';

let manager: UserManager | undefined;

export function getUserManager(): UserManager {
  if (typeof window === 'undefined') {
    throw new Error('Cognito authentication is only available in the browser.');
  }
  if (manager) return manager;

  const authority = process.env.NEXT_PUBLIC_COGNITO_ISSUER;
  const clientId = process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID;
  const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? window.location.origin;

  if (!authority || !clientId) {
    throw new Error('Cognito is not configured. Set NEXT_PUBLIC_COGNITO_ISSUER and NEXT_PUBLIC_COGNITO_CLIENT_ID.');
  }

  manager = new UserManager({
    authority,
    client_id: clientId,
    redirect_uri: new URL('/auth/callback', appUrl).toString(),
    post_logout_redirect_uri: new URL('/auth/signed-out', appUrl).toString(),
    response_type: 'code',
    scope: 'openid email profile',
    userStore: new WebStorageStateStore({ store: window.sessionStorage }),
    stateStore: new WebStorageStateStore({ store: window.sessionStorage }),
    automaticSilentRenew: true,
    monitorSession: false,
    loadUserInfo: false,
    filterProtocolClaims: true,
  });

  return manager;
}

export function getCognitoLogoutUrl(): string {
  const domain = process.env.NEXT_PUBLIC_COGNITO_DOMAIN;
  const clientId = process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID;
  const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? window.location.origin;
  if (!domain || !clientId) {
    throw new Error('Set NEXT_PUBLIC_COGNITO_DOMAIN and NEXT_PUBLIC_COGNITO_CLIENT_ID to enable logout.');
  }
  const logoutUrl = new URL('/logout', domain.startsWith('http') ? domain : `https://${domain}`);
  logoutUrl.searchParams.set('client_id', clientId);
  logoutUrl.searchParams.set('logout_uri', new URL('/auth/signed-out', appUrl).toString());
  return logoutUrl.toString();
}
