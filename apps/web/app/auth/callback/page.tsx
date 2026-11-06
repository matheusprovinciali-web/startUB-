'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getUserManager } from '../../../lib/oidc';

export default function AuthCallbackPage() {
  const router = useRouter();
  const [message, setMessage] = useState('Completing secure sign-in…');

  useEffect(() => {
    let active = true;
    getUserManager().signinRedirectCallback()
      .then(() => {
        if (active) router.replace('/');
      })
      .catch(() => {
        if (active) setMessage('Sign-in could not be completed. Return to StarUB Hub and try again.');
      });
    return () => { active = false; };
  }, [router]);

  return <main className="auth-page"><div className="auth-panel"><span className="brand-mark">S</span><h1>StarUB Hub</h1><p role="status">{message}</p><a href="/">Return to workspace</a></div></main>;
}
