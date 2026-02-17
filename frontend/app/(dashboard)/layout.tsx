import type { ReactNode } from "react";

import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="grid min-h-screen grid-cols-1 md:grid-cols-[260px_1fr]">
      <Sidebar />
      <section className="p-6">{children}</section>
    </div>
  );
}
