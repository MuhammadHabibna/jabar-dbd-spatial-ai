// app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AIDES Jawa Barat | AI Dengue Early-warning System",
  description: "Dashboard AI-powered Early Warning System untuk Demam Berdarah Dengue di Jawa Barat berbasis Precision Public Health",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
