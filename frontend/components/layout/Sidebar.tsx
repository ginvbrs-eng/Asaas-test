import Link from "next/link";

import { OrgSwitcher } from "@/components/layout/OrgSwitcher";

export function Sidebar() {
  return (
    <aside className="border-r bg-white p-4">
      <OrgSwitcher />
      <nav className="mt-6 space-y-2">
        <Link className="block rounded px-3 py-2 hover:bg-slate-100" href="/inventory">Inventory</Link>
        <Link className="block rounded px-3 py-2 hover:bg-slate-100" href="/assets">Assets</Link>
        <Link className="block rounded px-3 py-2 hover:bg-slate-100" href="/settings">Settings</Link>
      </nav>
    </aside>
  );
}
