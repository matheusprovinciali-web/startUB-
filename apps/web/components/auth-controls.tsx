'use client';

import { useState } from 'react';
import { useAuth } from './auth-provider';
import { getCognitoLogoutUrl } from '../lib/oidc';

export function AuthControls() {
  const { status, user, manager, error } = useAuth();
  const [busy, setBusy] = useState(false);

  async function signIn() {
    if (!manager) return;
    setBusy(true);
    try {
      await manager.signinRedirect();
    } catch {
      setBusy(false);
    }
  }

  async function signOut() {
    if (!manager) return;
    setBusy(true);
    try {
      await manager.removeUser();
      window.location.assign(getCognitoLogoutUrl());
    } catch {
      setBusy(false);
    }
  }

  if (status === 'loading') return <span className="auth-status">Checking session…</span>;
  if (status === 'error') return <span className="auth-error" role="status">{error ?? 'Sign-in unavailable'}</span>;
  if (status === 'authenticated' && user) {
    return <div className="auth-controls">
      <span className="auth-identity">{user.profile.email ?? user.profile.sub}</span>
      <button className="auth-button secondary" onClick={signOut} disabled={busy}>{busy ? 'Signing out…' : 'Sign out'}</button>
    </div>;
  }
  return <button className="auth-button" onClick={signIn} disabled={!manager || busy}>{busy ? 'Redirecting…' : 'Sign in'}</button>;
}
