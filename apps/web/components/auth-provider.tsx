'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import type { User, UserManager } from 'oidc-client-ts';
import { getUserManager } from '../lib/oidc';

type AuthState = {
  status: 'loading' | 'authenticated' | 'unauthenticated' | 'error';
  user: User | null;
  error: string | null;
  manager: UserManager | null;
};

const AuthContext = createContext<AuthState>({
  status: 'loading',
  user: null,
  error: null,
  manager: null,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [manager, setManager] = useState<UserManager | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<AuthState['status']>('loading');

  useEffect(() => {
    let active = true;
    let instance: UserManager;
    try {
      instance = getUserManager();
      setManager(instance);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Authentication configuration error.');
      setStatus('error');
      return;
    }

    const onLoaded = (nextUser: User) => {
      if (!active) return;
      setUser(nextUser);
      setStatus(nextUser.expired ? 'unauthenticated' : 'authenticated');
    };
    const onUnloaded = () => {
      if (!active) return;
      setUser(null);
      setStatus('unauthenticated');
    };
    const onRenewError = () => {
      if (!active) return;
      setUser(null);
      setStatus('unauthenticated');
    };

    instance.events.addUserLoaded(onLoaded);
    instance.events.addUserUnloaded(onUnloaded);
    instance.events.addSilentRenewError(onRenewError);
    instance.getUser()
      .then((current) => {
        if (!active) return;
        if (current && !current.expired) onLoaded(current);
        else {
          setUser(null);
          setStatus('unauthenticated');
        }
      })
      .catch((cause: unknown) => {
        if (!active) return;
        setError(cause instanceof Error ? cause.message : 'Could not restore the sign-in session.');
        setStatus('error');
      });

    return () => {
      active = false;
      instance.events.removeUserLoaded(onLoaded);
      instance.events.removeUserUnloaded(onUnloaded);
      instance.events.removeSilentRenewError(onRenewError);
    };
  }, []);

  const value = useMemo(() => ({ status, user, error, manager }), [status, user, error, manager]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
