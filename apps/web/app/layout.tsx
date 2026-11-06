import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'StarUB Hub',
  description: 'Innovation Hub Operating System',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
