import type { Metadata } from "next";
import "./globals.css";

import { QueryProvider } from "@/components/providers/QueryProvider";

export const metadata: Metadata = {
  title: "ASAAS Platform",
  description: "Modular business management SaaS",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fr">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
