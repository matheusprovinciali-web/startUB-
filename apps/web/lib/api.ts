'use client';

import { getUserManager } from './oidc';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function apiFetch(path: string, init: RequestInit = {}, tenantId?: string): Promise<Response> {
  if (!API_BASE_URL) throw new Error('NEXT_PUBLIC_API_BASE_URL is not configured.');
  const user = await getUserManager().getUser();
  if (!user || user.expired || !user.access_token) {
    throw new Error('Your StarUB Hub session has expired. Please sign in again.');
  }

  const headers = new Headers(init.headers);
  headers.set('Authorization', `Bearer ${user.access_token}`);
  if (tenantId) headers.set('X-Tenant-ID', tenantId);
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');

  return fetch(new URL(path.replace(/^\//, ''), `${API_BASE_URL.replace(/\/$/, '')}/`), {
    ...init,
    headers,
    cache: 'no-store',
  });
}
