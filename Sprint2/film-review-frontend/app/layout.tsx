import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Film Review Platform - Host Portal',
  description: 'Companion Next.js frontend embedding FastAPI /ui/films via iframe',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
